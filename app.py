from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
from entities.user import User

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        # Here you would normally verify the email and password
        # For demonstration, we will just log in any user
        user = User.check_login(email, password)  # You would replace this with your actual user retrieval logic
        
        
        if user and user.is_active:
            login_user(user)
            return jsonify({'success' : True, "message": "Logged in successfully!",}), 200
        else:   
            return jsonify({'success' : False, 'message' : "Invalid request", }), 401   

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', email=current_user.email)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

if __name__ == '__main__':
    app.run(port=5000)