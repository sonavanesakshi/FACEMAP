from flask import Flask, render_template, redirect, request, jsonify, Response
from realtime_detection import *
from symptom_based import *
import subprocess
import atexit
import signal
from datetime import datetime
from backend.db_helper import *

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REALTIME_FOLDER = os.path.join(UPLOAD_FOLDER, "realtime")
SYMPTOM_FOLDER = os.path.join(UPLOAD_FOLDER, "symptom_based")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REALTIME_FOLDER"] = REALTIME_FOLDER
app.config["SYMPTOM_FOLDER"] = SYMPTOM_FOLDER
streamlit_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = login_user(username, password)

    if user:
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials."})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    sign_up = signup_user(username, password)
    if sign_up == -1:
        return jsonify({"success": False, "message": "Something went wrong!"})

    return jsonify(sign_up)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/realtime/analyze", methods=["POST"])
def analyze():
    req_data = request.get_json()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"skin_analysis_{timestamp}.jpg"
    file_path = os.path.join(app.config["REALTIME_FOLDER"], filename)
    return jsonify(analyze_skin(req_data, file_path, filename))

@app.route("/realtime/suggestions", methods=["POST"])
def suggestions():
    req_data = request.get_json()
    return jsonify(get_suggestions(req_data))

@app.route("/realtime/download", methods=["POST"])
def download():
    try:
        data = request.get_json()

        pdf_file_path = generate_pdf(data)
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()

        response = Response(pdf_content)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=Skin_Analysis_Report.pdf"
        return response

    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/realtime')
def realtime_streamlit():
    return render_template('realtime.html')

@app.route('/symptoms')
def symptoms_streamlit():
    return render_template('symptoms.html')

@app.route('/symptoms/list')
def symptoms_list():
    return jsonify(get_symptoms_list())

# Predict acne type from image
@app.route("/predict_image", methods=["POST"])
def predict_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    file_path = os.path.join(app.config["SYMPTOM_FOLDER"], file.filename)
    file.save(file_path)

    result = predict_acne_from_image(file_path, file.filename)

    return jsonify(result)

@app.route("/predict_symptoms", methods=["POST"])
def predict_symptoms():
    input_symptoms = request.json.get("symptoms", "")
    return jsonify(predict_acne(input_symptoms))

if __name__ == '__main__':
    app.run(debug=True, port=5000)