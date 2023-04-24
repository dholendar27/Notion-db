from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import main
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "V3C#v!955"
CORS(app)

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        openai_api_key = request.form.get('Openai_key')
        notion_token = request.form.get('Notion_token')
        database_id = request.form.get('Database_id')
        main.openai_api_key = openai_api_key
        main.NOTION_TOKEN = notion_token
        main.DATABASE_ID = database_id
        main.Embeddings()
        session['fields_filled'] = True
        # Log in the user
        user = User(1)
        login_user(user)
        return redirect(url_for('chatbot'))
    return render_template('index.html')

@app.route('/chatbot', methods=['GET'])
@login_required
def chatbot():
    return render_template('chatbot.html')

@app.route('/data', methods=['GET'])
@login_required
def data():
    question = request.args.get('chat')
    result = main.response(question)
    return result

@app.route('/logout')
@login_required
def logout():
    # Log out the user
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="10.10.20.171",debug=True)
