from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'porsche911'

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Home Page"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    return render_template('index.html', board=board, highscore=highscore, numplays=numplays)
    

@app.route('/check-word')
def check_word():
    """Checking the words"""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/post-score',methods=['POST'])
def post_score():
    """Get score, update number of plays and update highest score"""

    score = request.json['score']
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    session['highscore'] = max(score, highscore)
    session['numplays'] = numplays + 1

    return jsonify(brokeRecord=score > highscore)
    
