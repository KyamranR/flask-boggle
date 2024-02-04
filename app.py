from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle



app = Flask(__name__)
app.config['SECRET_KEY'] = 'porsche911'

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Home Page"""
    
    return render_template('index.html')
    