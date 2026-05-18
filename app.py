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

        user = User.check_login(email, password)  
        
        
        if user and user.is_active:
            login_user(user)
            
            session['user_id'] = user.id 
            session['permissions'] = [p.value for p in user.permissions] 
            
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
        'lives': 3
    }

    first_word = words[0]

    return jsonify({
        'success': True,
        'hint': first_word.hint,
        'question': 1,
        'lives': 3
    })
    
@app.route('/api/game/answer', methods=['POST'])
@login_required
def answer():
    data = request.get_json()
    
    answer = data.get('answer')
    game = session.get('game')
    
    current_index = game['current']
    question_id = game['questions'][current_index]
    
    #word = Word.get_by_id(question_id)

    if Word.check_word(question_id, answer.lower()):
        
        new_word = Word.get_by_id(game['questions'][game['current'] + 1]) if game['current'] + 1 < len(game['questions']) else None

        game['current'] += 1

        session['game'] = game

        return jsonify({
            'correct': True,
            'current' : game['current'],
            'hint': new_word.hint if new_word else None
        })

    else:

        game['lives'] -= 1

        session['game'] = game

        return jsonify({
            'correct': False,
            'lives': game['lives'],
        })
        
@app.route('/edit_riddles')
@login_required
def edit_riddles():
    
    if 1 not in session.get('permissions'):
        return redirect(url_for('welcome'))
    
    words = Word.get_all_words()
    
    return render_template('edit_riddles.html', words=words)    


@app.route("/admin/riddles/create", methods=["POST"])
def create_riddle():
    hint = request.form.get("hint")
    word = request.form.get("word")
    
    if Word.create(word, hint):
        return redirect(url_for('edit_riddles'))


@app.route("/admin/riddles/edit/<int:id>", methods=["POST"])
def edit_riddle(id):
    hint = request.form.get("hint")
    word = request.form.get("word")

    if Word.edit(id, word, hint):
        return redirect(url_for('edit_riddles'))


@app.route("/admin/riddles/delete/<int:id>", methods=["POST"])
def delete_riddle(id):
    if Word.delete(id):
        return redirect(url_for('edit_riddles'))


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