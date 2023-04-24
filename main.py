from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain .document_loaders import NotionDBLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import tiktoken
import os

load_dotenv()
NOTION_TOKEN = ""
DATABASE_ID = ""
openai_api_key = ""

persist_directory = 'db'
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
encoding = tiktoken.encoding_for_model('davinci')
tokenizer = tiktoken.get_encoding(encoding.name)

def tk_len(text):
    token = tokenizer.encode (
        text,
        disallowed_special=()
    )
    return len(token)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=20,
    length_function=tk_len,
    separators=['\n\n','\n',',','']
)

def Embeddings():
    loader = NotionDBLoader(NOTION_TOKEN, DATABASE_ID)
    docs = loader.load()
    chunks = text_splitter.split_documents(docs)
    Chroma.from_documents(chunks, embeddings,persist_directory=persist_directory)

def response(query):
    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
    assist = RetrievalQA.from_llm(OpenAI(temperature=0, model_name="text-davinci-003",openai_api_key=openai_api_key),
                                                retriever=db.as_retriever())
    response = assist(query)
    return response['result']
