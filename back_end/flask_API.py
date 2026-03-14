from flask import Flask , jsonify , request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from main import quizzes
from read_pdf import get_text_from_pdf
from main import generate_quizzes

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])

@app.route("/")
def home() :
    return "home"


# @app.route("/quizzes")
# def get_quizzes() :
#     Quizzes = quizzes
#     return jsonify(Quizzes)



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
        return {
            "message": "File uploaded successfully",
            "filename": filename}, 200
    else :
        return {'error': 'File type not allowed'}, 400




# genarate_quizzes
@app.route("/generate_quizzes", methods=["POST"])
def generate_quizzes_route():
    data = request.get_json()
    if not data:
        return {"error": "No JSON data received"}, 400
    filename = data.get("filename")
    if not filename:
        return {"error": "no pdf file to generate"}, 400
    if not filename.endswith(".pdf"):
        return {"error": "file must be pdf"}, 400
    try:
        text = get_text_from_pdf(filename)
        res = generate_quizzes.invoke({
            "context": text,
            "num_quizs": 3
        })
        return jsonify(res), 200
    except Exception as e:
        return {"error": str(e)}, 500




# @app.route("/test/results/<test_result>")
# def user(test_result) :
#     try :
#       for elem in test_result.results :
#         return elem
#     except :
#        return "error !"


if __name__ == "__main__" :
    app.run(debug=True)