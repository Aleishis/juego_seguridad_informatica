from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os
from entities.user import User
from entities.word import Word

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

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
            
            session['user_id'] = user.id  
            
            return jsonify({'success' : True, "message": "Logged in successfully!",}), 200
        else:   
            return jsonify({'success' : False, 'message' : "Invalid request", }), 401   

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/api/signup',methods=['POST'])
def register():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.save(name, email, password):
        return jsonify({'success' : True, "message": "User registered successfully!"}), 201
    else:
        return jsonify({'success' : False, 'message' : "Error saving user"}), 403
    
    
@app.route('/welcome')
@login_required
def welcome():    
    return render_template('welcome.html', username=current_user.name)

@app.route('/api/game/start', methods=['POST'])
@login_required
def start_game():

    words = Word.get_random_words()

    session['game'] = {
        'questions': [word.id for word in words],
        'current': 0,
        'score': 0,
        'lives': 3
    }

    first_word = words[0]

    return jsonify({
        'success': True,
        'hint': first_word.hint,
        'question': 1,
        'lives': 3
    })

@app.route('/game')
@login_required
def game():
    return render_template('game.html')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)