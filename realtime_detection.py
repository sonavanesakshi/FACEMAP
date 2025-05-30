import cv2
import numpy as np
# import streamlit as st
import pandas as pd
from fpdf import FPDF
from backend.db_helper import *
import base64
import json

# Load pre-trained models
age_model = cv2.dnn.readNetFromCaffe(
    r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\age_deploy.prototxt",
    r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\age_net.caffemodel"
)
gender_model = cv2.dnn.readNetFromCaffe(
    r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\gender_deploy.prototxt",
    r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\gender_net.caffemodel"
)
face_detector = cv2.dnn.readNetFromTensorflow(
    r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\opencv_face_detector_uint8.pb",
    r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\opencv_face_detector.pbtxt"
)

# Labels for predictions
age_labels = ['(0-3)', '(4-6)', '(7-13)', '(14-20)', '(21-24)', '(25-32)', '(33-37)', '(38-43)', '(44-47)', '(48-50)', 
              '(51-59)', '(60-100)']
gender_labels = ['Male', 'Female']

# Load skincare suggestions from CSV
# csv_path = r"C:\Users\Lenovo\Desktop\SKIN ANALYSIS\dataset\enhanced_ayurvedic_acne_dataset.csv"  # Path to your CSV file
csv_path = r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\ayurvedic_acne_care_dataset.csv"  # Path to your CSV file
acne_data = pd.read_csv(csv_path)

# Clean up column names by stripping leading/trailing spaces
acne_data.columns = acne_data.columns.str.strip()

# Skin type prediction function
def predict_skin_type(symptoms):
    matching_rows = []

    # Loop through the dataset and check for symptom matches
    for _, row in acne_data.iterrows():
        acne_symptoms = [sym.strip().lower() for sym in row['Symptoms'].split(',')]
        matched = sum(1 for symptom in symptoms if symptom.lower() in acne_symptoms)
        if matched > 0:  # At least one symptom matches
            matching_rows.append(row)

    # Aggregate results if matches are found
    if matching_rows:
        combined_suggestions = {
            "Breakfast": set(),
            "Lunch": set(),
            "Dinner": set(),
            "Detox Drinks": set(),
            "Skincare": set(),
            "Home Remedies": set()
        }
        for row in matching_rows:
            combined_suggestions["Breakfast"].add(row['Breakfast'])
            combined_suggestions["Lunch"].add(row['Lunch'])
            combined_suggestions["Dinner"].add(row['Dinner'])
            combined_suggestions["Detox Drinks"].add(row['Detox Drinks'])
            combined_suggestions["Skincare"].add(row['Skincare Recommendations'])
            combined_suggestions["Home Remedies"].add(row['Home Remedies'])

        # Convert sets to strings for display
        for key in combined_suggestions:
            combined_suggestions[key] = ', '.join(combined_suggestions[key])

        return matching_rows[0]['Acne Type'], combined_suggestions
    else:
        return "Unknown", {"Message": "No matching acne type found."}

# PDF report generation
def generate_report(gender, age, acne_type, suggestions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Skin Analysis Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Acne Type: {acne_type}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Skincare Recommendations:", ln=True)
    for key, value in suggestions.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    report_file = "Skin_Analysis_Report.pdf"
    pdf.output(report_file)
    return report_file

# # Initialize session state variables
# if 'image_captured' not in st.session_state:
#     st.session_state.image_captured = False
# if 'analysis_done' not in st.session_state:
#     st.session_state.analysis_done = False
# if 'gender' not in st.session_state:
#     st.session_state.gender = None
# if 'age' not in st.session_state:
#     st.session_state.age = None
# if 'acne_type' not in st.session_state:
#     st.session_state.acne_type = None
# if 'suggestions' not in st.session_state:
#     st.session_state.suggestions = None

# # Streamlit UI
# st.title("AI-Based Skin Analysis System")

# # Step 1: Capture an image
# st.header("Step 1: Capture Image")
# capture_image = st.button("Capture Image")

# if capture_image:
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     if ret:
#         cv2.imwrite("captured_image.jpg", frame)
#         st.image("captured_image.jpg", caption="Captured Image", use_column_width=True)
#         st.success("Image Captured!")
#         st.session_state.image_captured = True
#     else:
#         st.error("Failed to capture image.")
#     cap.release()

# # Step 2: Analyze Skin
# st.header("Step 2: Analyze Skin")
# analyze_skin = st.button("Analyze Skin")
def analyze_skin(data, file_path, filename):
    image_data = data["image"].split(",")[1]
    image_array = np.frombuffer(base64.b64decode(image_data), dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    h, w = frame.shape[:2]

    cv2.imwrite(file_path, frame)

    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    face_detector.setInput(blob)
    detections = face_detector.forward()

    error = 'Something went wrong'
    gender = 'Not detected'
    age = 'Not detected'
    acne_type = 'Not detected'

    if detections.shape[2] > 0:
        max_confidence_idx = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, max_confidence_idx, 2]

        if confidence > 0.6:
            box = detections[0, 0, max_confidence_idx, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype(int)
            face = frame[y1:y2, x1:x2]

            if face.shape[0] > 30 and face.shape[1] > 30:
                face_blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), [104, 117, 123], swapRB=False)
                gender_model.setInput(face_blob)
                gender = gender_labels[gender_model.forward()[0].argmax()]
                age_model.setInput(face_blob)
                age = age_labels[age_model.forward()[0].argmax()]
                symptoms = ["reddish eruptions", "oily"]
                acne_type, suggestions = predict_skin_type(symptoms)
                
                insert_analysis_results(gender, age, acne_type, suggestions, filename)
            else:
                error = "Face size too small for analysis."

        else:
            error = "No confident face detected."
        return {"gender": gender, "age": age, "acne_type": acne_type }
    else:
        error = "No face detected."
    
    return {"error": error}

def get_suggestions(data):
    gender = data["gender"]
    age = data["age"]
    acne_type = data["acne_type"]
    result = {}
    symptoms = ["reddish eruptions", "oily"]
    acne_type, suggestions = predict_skin_type(symptoms)
    if "Message" in suggestions:
        result = { "error": suggestions["Message"] }
    else:
        for key, value in suggestions.items():
            result[key] = value
    return result

def generate_pdf(data):
    gender = data["gender"]
    age = data["age"]
    acne_type = data["acne_type"]
    symptoms = ["reddish eruptions", "oily"]
    acne_type, suggestions = predict_skin_type(symptoms)
    data["suggestions"] = suggestions
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Skin Analysis Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Gender: {data['gender']}", ln=True)
    pdf.cell(200, 10, txt=f"Age Group: {data['age']}", ln=True)
    pdf.cell(200, 10, txt=f"Acne Type: {data['acne_type']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Suggestions", ln=True)
    pdf.ln(5)

    suggestions = data["suggestions"]

    for category, suggestions_str in suggestions.items():
        suggestion_list = json.loads(suggestions_str.replace("'", "\""))

        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 8, txt=f"{category}:", ln=True)
        pdf.set_font("Arial", size=11)

        for suggestion in suggestion_list:
            pdf.multi_cell(0, 7, txt=f"- {suggestion}")
        pdf.ln(3)

    pdf_file_path = "report.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path



# if analyze_skin and st.session_state.image_captured:
#     frame = cv2.imread("captured_image.jpg")
#     h, w = frame.shape[:2]
#     blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
#     face_detector.setInput(blob)
#     detections = face_detector.forward()

#     if detections.shape[2] > 0:
#         max_confidence_idx = np.argmax(detections[0, 0, :, 2])
#         confidence = detections[0, 0, max_confidence_idx, 2]

#         if confidence > 0.6:
#             box = detections[0, 0, max_confidence_idx, 3:7] * np.array([w, h, w, h])
#             (x1, y1, x2, y2) = box.astype(int)
#             face = frame[y1:y2, x1:x2]

#             if face.shape[0] > 30 and face.shape[1] > 30:
#                 face_blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), [104, 117, 123], swapRB=False)
#                 gender_model.setInput(face_blob)
#                 st.session_state.gender = gender_labels[gender_model.forward()[0].argmax()]
#                 age_model.setInput(face_blob)
#                 st.session_state.age = age_labels[age_model.forward()[0].argmax()]
#                 symptoms = ["reddish eruptions", "oily"]  # Example symptoms
#                 st.session_state.acne_type, st.session_state.suggestions = predict_skin_type(symptoms)
#                 st.session_state.analysis_done = True
#                 st.success("Analysis Completed!")
#             else:
#                 st.warning("Face size too small for analysis.")
#         else:
#             st.error("No confident face detected.")
#     else:
#         st.error("No face detected.")

# # Display analysis results
# if st.session_state.analysis_done:
#     st.write(f"Gender: {st.session_state.gender}")
#     st.write(f"Age: {st.session_state.age}")
#     st.write(f"Acne Type: {st.session_state.acne_type}")
#     if st.button("Show Suggestions"):
#         suggestions = st.session_state.suggestions
#         if "Message" in suggestions:
#             st.write(suggestions["Message"])
#         else:
#             for key, value in suggestions.items():
#                 st.write(f"{key}: {value}")
#     if st.button("Generate PDF Report"):
#         report_file = generate_report(
#             st.session_state.gender,
#             st.session_state.age,
#             st.session_state.acne_type,
#             st.session_state.suggestions
#         )
#         st.success(f"Report saved as {report_file}")

# if st.button("Back"):
#     st.markdown("""
#         <meta http-equiv="refresh" content="0;URL='http://localhost:5000'" />
#     """, unsafe_allow_html=True)