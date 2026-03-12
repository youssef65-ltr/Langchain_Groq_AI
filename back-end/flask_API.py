from flask import Flask , jsonify , request
from flask_cors import CORS
from werkzeug.utils import secure_filename
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



# upload PDF :
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/uploadpdf", methods=["POST"])
def upload_pdf() :
    if 'file' not in request.files:
        return {'error': 'No file part in the request'}, 400
    file = request.files["file"]
    if file.filename == '':
        return {'error': 'No selected file'}, 400 
    
    if file :
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return {"message": "File uploaded successfully", "filename": filename}, 200
    else :
        return {'error': 'File type not allowed'}, 400





# @app.route("/test/results/<test_result>")
# def user(test_result) :
#     try :
#       for elem in test_result.results :
#         return elem
#     except :
#        return "error !"

    
        



if __name__ == "__main__" :
    app.run(debug=True)