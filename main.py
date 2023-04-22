from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain .document_loaders import NotionDBLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv
import tiktoken
import os

load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('DATABASE_ID')


persist_directory = 'db'
embeddings = OpenAIEmbeddings()
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
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("db/faiss_index")

def response(query):
    db = FAISS.load_local("db/faiss_index", embeddings)
    assist = RetrievalQA.from_llm(OpenAI(temperature=0, model_name="text-davinci-003"),
                                                retriever=db.as_retriever())
    response = assist(query)
    return response['result']
