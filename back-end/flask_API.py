from flask import Flask , jsonify
from flask_cors import CORS
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import quizzes

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route("/")
def home() :
    return "home"


@app.route("/quizzes")
def get_quizzes() :
    Quizzes = quizzes
    return jsonify(Quizzes)



if __name__ == "__main__" :
    app.run(debug=True)