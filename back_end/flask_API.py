from flask import Flask , jsonify , request, session
from flask_cors import CORS
from datetime import timedelta 
from werkzeug.utils import secure_filename
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# mongoDB :
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps
# mysql :
import pymysql

# from main import quizzes
from read_pdf import get_text_from_pdf
from main import generate_quizzes


app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(days=15)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# connect to mongoDB :
client = MongoClient(host="localhost" , port=27017)
db = client["smart_learning"]
# connect to mysql :

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='smart_learning',
    port=3306,                          # default MySQL port
    cursorclass=pymysql.cursors.DictCursor  # results as dicts
)

# Dict cursor → dicts (recommended)
cursor = conn.cursor(pymysql.cursors.DictCursor)


# users = cursor.fetchall()       # all rows
# user  = cursor.fetchone()       # single row
# some  = cursor.fetchmany(5)     # 5 rows





# upload PDF from user :
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


# function to generate primary key in mongoDB :
def get_next_id():
    last = db.TestCollection.find_one(
        sort=[("_id", -1)]  # get the biggest _id
    )
    return (last["_id"] + 1) if last else 1



# genarate_quizzes from test_extracted and store a test in mongoDB :
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
        db.TestCollection.insert_one({
            "test_id" : get_next_id(),
            "pdf_title" : str(filename) ,
            "quizzes" : res ,
            "questions_true" : 0,
            "questions_false" : 0
        })
        return jsonify({"message" : "success"}), 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 500

# do an specific test :
@app.route("/start_test/<id>", methods=["GET"])
def start_test(id):
    doc = db.TestCollection.find_one({"test_id" : int(id)})
    if not doc:
        return jsonify({"error": "Test not found"}), 404
    return dumps(doc), 200, {"Content-Type": "application/json"}


# login :
@app.route("/login" , methods=["POST"])
def login():
    data = request.get_json()
    if not data :
        return jsonify({"error" : "No JSON data received"}), 400
    email = data.get("email")
    password_hash = data.get("password_hash")

    if (email == "" or password_hash == "") : 
        return jsonify({"error" : "Data is not valid"}) , 400
    cursor.execute("select * from user where email=%s and password_hash=%s" , (email , password_hash))
    user = cursor.fetchone()
    if user is None :
        return jsonify({"error" : "this user is not exist or either the email or password are not valid"}), 400
    
    session['user_id']   = user['user_id']
    session['username'] = user['username']
    session['logged_in'] = True
    return jsonify({"message" : f"login success"}) , 200


# sing in ;
@app.route("/singin", methods=["POST"])
def singin():
    data = request.get_json()
    if not data : 
        return jsonify({"error": "No JSON data received"}), 400
    username = data.get("username")
    email = data.get("email")
    password_hash = data.get("password_hash")

    if (username == "" or email == "" or password_hash == "") : 
        return jsonify({"error" : "Data is not valid"}) , 400
    cursor.execute("select * from user where username=%s or email=%s" , (username, email))
    users = cursor.fetchall()
    if  len(users) != 0 :
        return jsonify({"error" : "user already exists"}) , 400
    else :
        cursor.execute("insert into user(username, email, password_hash) values ( %s, %s, %s)",
                        (username , email , password_hash))
        conn.commit()
        if cursor.lastrowid != "" : 
            # create session :
            session["user_id"] = cursor.lastrowid
            session['username'] = username
            session['logged_in'] = True
            return jsonify({"message" : "singin success"}) , 200


@app.route("/session_profil" , methods=["GET"])
def session_profil():
        if session.get('logged_in') :
            return jsonify({'username': session['username'],
                             'user_id': session['user_id'],
                             'logged_in': session['logged_in']})
        else :
            return jsonify({'message': 'Unauthorized'}), 401

@app.route("/logout", methods=["GET"])
def logout():
    session.clear() 
    return jsonify({'message': 'Logged out'})


if __name__ == "__main__" :
    app.run(debug=True)