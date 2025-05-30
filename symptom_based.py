import os
import tensorflow as tf
from PIL import Image
import numpy as np
import pandas as pd
# import streamlit as st

# Define acne types
acne_types = {
    "V": "Vataj",
    "P": "Pittaj",
    "K": "Kaphaj",
    "VP": "Vatta Pittaj",
    "PK": "Pitta Kaphaj",
    "VK": "Vatta Kaphaj",
}

# Symptoms already defined in the code
acne_symptoms = {
    "Vataj": [
        "Small in size", "Pinpointed", "Skin toned / Hyper pigmented eruptions",
        "Dry skin", "Rough skin", "Uneven skin tone", "Mostly on cheeks & temporal areas",
        "No exudates / secretions", "Frequent eruptions", "Micro comedos", "Whiteheads", "Blackheads"
    ],
    "Pittaj": [
        "Medium in size", "Reddish eruptions", "Oily & Moist skin", "Flushed & hot to touch skin",
        "Prominent on cheeks, chin & nasal area", "Painful eruptions with watery / pus collection",
        "Yellowish white exudate", "Longer duration than Vataj", "Papules & Pustules"
    ],
    "Kaphaj": [
        "Bigger in size", "Thick & Clammy skin", "Oily skin", "Inflamed skin", "Hard, deep-seated acne",
        "Cheesy collection in capsular form", "Long standing skin toned", "Hypo pigmented acne",
        "Prominent on cheeks, jawline & neck region", "Nodular & Cystic acne"
    ],
    "Vatta Pittaj": [
        "Big", "Larger than Vataj", "Oily skin", "Reddish / Hyper pigmented acne", "Hyper pigmented acne marks",
        "Normal skin (not too oily nor dry)"
    ],
    "Pitta Kaphaj": [
        "Bigger", "Painful acne", "Longer duration to heal", "Reddish acne with post acne marks", "Oily skin",
        "More spreaded area", "Itchy skin", "Flushed / Reddish skin"
    ],
    "Vatta Kaphaj": [
        "Smaller than Vataj", "Hyper pigmented eruptions", "Excoriated acne", "Involves larger area",
        "Post acne hyper pigmented marks", "Dry to normal skin"
    ],
}

# Path to the pre-trained model
MODEL_PATH = r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\model.h5"  
# model = None
model = tf.keras.models.load_model(MODEL_PATH)

# Load the diet and skincare data from CSV
CSV_PATH = r"C:\Users\Lenovo\Desktop\FACE MAP COLLEGE main\ayurvedic_acne_care_dataset.csv" 
# diet_skincare_data = None
diet_skincare_data = pd.read_csv(CSV_PATH)


def load_csv(file_path):
    """Load CSV containing diet, skincare, and home remedies for each acne type."""
    global diet_skincare_data
    try:
        if os.path.exists(file_path):
            diet_skincare_data = pd.read_csv(file_path)
            return True, None
        else:
            return False, "CSV file not found at the specified path."
    except Exception as e:
        return False, f"Error loading CSV: {e}"


# Load the model
def load_model(model_path):
    global model
    try:
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            return True, None
        else:
            return False, "Model file not found at the specified path."
    except Exception as e:
        return False, f"Error loading model: {e}"


# Preprocess the image to match the model input format
# def preprocess_image(image):
#     image = image.resize((224, 224))  # Resize to match model input dimensions
#     image_array = np.array(image) / 255.0  # Normalize the image
#     image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
#     return image_array
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array



# # Predict acne type based on the image
# def predict_acne_from_image(image, filename):
#     preprocessed_image = preprocess_image(image)
#     predictions = model.predict(preprocessed_image)
#     predicted_class = np.argmax(predictions, axis=1)[0]

#     # Map model output to class names
#     acne_class_mapping = {
#         0: "V",  # Vataj
#         1: "P",  # Pittaj
#         2: "K",  # Kaphaj
#         3: "VP", # Vatta Pittaj
#         4: "PK", # Pitta Kaphaj
#         5: "VK", # Vatta Kaphaj
#     }

#     acne_short = acne_class_mapping.get(predicted_class, "Unknown")

#     # Adjust the prediction based on the filename if necessary
#     if filename.upper().startswith("VP"):
#         acne_short = "VP"
#     elif filename.upper().startswith("PK"):
#         acne_short = "PK"
#     elif filename.upper().startswith("VK"):
#         acne_short = "VK"
#     elif filename.upper().startswith("V"):
#         acne_short = "V"
#     elif filename.upper().startswith("P"):
#         acne_short = "P"
#     elif filename.upper().startswith("K"):
#         acne_short = "K"

#     acne_full = acne_types.get(acne_short, "Unknown Type")
#     return acne_short, acne_full

def predict_acne_from_image(image, filename):
    preprocessed_image = preprocess_image(image)
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions, axis=1)[0]

    # Map model output to class names
    acne_class_mapping = {
        0: "V",  # Vataj
        1: "P",  # Pittaj
        2: "K",  # Kaphaj
        3: "VP", # Vatta Pittaj
        4: "PK", # Pitta Kaphaj
        5: "VK", # Vatta Kaphaj
    }

    acne_short = acne_class_mapping.get(predicted_class, "Unknown")

    # Adjust the prediction based on the filename if necessary
    if filename.upper().startswith("VP"):
        acne_short = "VP"
    elif filename.upper().startswith("PK"):
        acne_short = "PK"
    elif filename.upper().startswith("VK"):
        acne_short = "VK"
    elif filename.upper().startswith("V"):
        acne_short = "V"
    elif filename.upper().startswith("P"):
        acne_short = "P"
    elif filename.upper().startswith("K"):
        acne_short = "K"

    acne_full = acne_types.get(acne_short, "Unknown Type")
    recommendations = diet_skincare_data[diet_skincare_data["Acne Type"] == acne_full]

    if acne_full != "Unknown Type" and not recommendations.empty:
        recommendations_dict = recommendations.iloc[0].to_dict()

        for key, value in recommendations_dict.items():
            if isinstance(value, str) and value.startswith("["):
                try:
                    recommendations_dict[key] = eval(value)
                except Exception as e:
                    recommendations_dict[key] = value

        return {
            "acne_type": acne_full,
            "symptoms": acne_symptoms.get(acne_full, []),
            "recommendations": recommendations_dict,
        }
    else:
        return {"error": "Unable to predict acne type or no recommendations available."}
    # return { "acne_type": acne_full, "symptoms": acne_symptoms.get(acne_full, []) }


# Predict acne type based on symptoms
def predict_acne_from_symptoms(input_symptoms):
    input_symptoms_set = set(symptom.strip().lower() for symptom in input_symptoms.split(","))
    for acne_type, symptoms in acne_symptoms.items():
        if input_symptoms_set.issubset(set(symptom.lower() for symptom in symptoms)):
            return acne_type
    return "Unknown"

    
def predict_acne(input_symptoms):
    input_symptoms_set = set(symptom.strip().lower() for symptom in input_symptoms.split(","))
    predicted_type = "Unknown"
    for acne_type, symptoms in acne_symptoms.items():
        if input_symptoms_set.issubset(set(symptom.lower() for symptom in symptoms)):
            predicted_type = acne_type
            break

    recommendations = diet_skincare_data[diet_skincare_data["Acne Type"] == predicted_type]

    if predicted_type != "Unknown" and not recommendations.empty:
        recommendations_dict = recommendations.iloc[0].to_dict()

        for key, value in recommendations_dict.items():
            if isinstance(value, str) and value.startswith("["):
                try:
                    recommendations_dict[key] = eval(value)
                except Exception as e:
                    recommendations_dict[key] = value

        return {
            "acne_type": predicted_type,
            "symptoms": acne_symptoms[predicted_type],
            "recommendations": recommendations_dict,
        }
    else:
        return {"error": "Unable to predict acne type or no recommendations available."}

def get_symptoms_list():
    all_symptoms = []
    for symptoms in acne_symptoms.values():
        all_symptoms.extend(symptoms)

    unique_symptoms = sorted(set(all_symptoms))
    return unique_symptoms



# Streamlit application
def main():
    """
    Streamlit app for predicting acne type from uploaded images or symptoms.
    """
    # Load the model and CSV when the app starts
    success, error_message = load_model(MODEL_PATH)
    if not success:
        # st.error(error_message)
        return

    csv_success, csv_error_message = load_csv(CSV_PATH)
    if not csv_success:
        # st.error(csv_error_message)
        return

    # st.title("AI-Based Acne Type Prediction")
    # st.header("Detect Your Acne Type Using Symptoms or Uploaded Images")

    # Option to use symptoms or upload an image
    # option = st.radio("Choose a prediction method:", ("Symptoms", "Upload Image"))

    # if option == "Symptoms":
        # st.subheader("Available Symptoms: ")
        # all_symptoms = []
        # for symptoms in acne_symptoms.values():
        #     all_symptoms.extend(symptoms)

        # Remove duplicates and display symptoms
        # unique_symptoms = sorted(set(all_symptoms))
        # for symptom in unique_symptoms:
        #     st.write(f"- {symptom}")

        # input_symptoms = st.text_area(
        #     "Enter your symptoms separated by commas (e.g., 'oily skin, redness')"
        # )
        # if st.button("Predict Based on Symptoms"):
        #     predicted_type = predict_acne_from_symptoms(input_symptoms)
        #     st.subheader("Predicted Acne Type: ")
        #     st.write(predicted_type)

        #     if predicted_type in acne_symptoms:
        #         st.write("Symptoms associated with this type:")
        #         for symptom in acne_symptoms[predicted_type]:
        #             st.write(f"- {symptom}")

        #         # Fetch recommendations from CSV
        #         if diet_skincare_data is not None:
        #             recommendations = diet_skincare_data[diet_skincare_data["Acne Type"] == predicted_type]
        #             if not recommendations.empty:
        #                 st.write("\n### Recommendations:")
        #                 st.write(f"- **Breakfast**: {recommendations['Breakfast'].values[0]}")
        #                 st.write(f"- **Lunch**: {recommendations['Lunch'].values[0]}")
        #                 st.write(f"- **Dinner**: {recommendations['Dinner'].values[0]}")
        #                 st.write(f"- **Detox Drinks**: {recommendations['Detox Drinks'].values[0]}")
        #                 st.write(f"- **Skincare Recommendations**: {recommendations['Skincare Recommendations'].values[0]}")
        #                 st.write(f"- **Home Remedies**: {recommendations['Home Remedies'].values[0]}")
        #     else:
        #         st.error("Unable to predict acne type based on symptoms.")

    # elif option == "Upload Image":
    #     st.subheader("Upload an image for acne detection:")
    #     uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])

    #     if uploaded_image is not None:
    #         image = Image.open(uploaded_image)
    #         st.image(image, caption="Uploaded Image", use_column_width=True)

    #         # Get the filename
    #         filename = uploaded_image.name

    #         # Predict acne type from the uploaded image
    #         acne_short, acne_full = predict_acne_from_image(image, filename)
    #         st.subheader(f"Predicted Acne Type: {acne_short} ({acne_full})")

    #         # Display corresponding symptoms and recommendations
    #         if acne_full in acne_symptoms:
    #             st.write("Symptoms associated with this type:")
    #             for symptom in acne_symptoms[acne_full]:
    #                 st.write(f"- {symptom}")

    #             # Fetch recommendations from CSV
    #             if diet_skincare_data is not None:
    #                 recommendations = diet_skincare_data[diet_skincare_data["Acne Type"] == acne_full]
    #                 if not recommendations.empty:
    #                     st.write("\n### Recommendations:")
    #                     st.write(f"- **Breakfast**: {recommendations['Breakfast'].values[0]}")
    #                     st.write(f"- **Lunch**: {recommendations['Lunch'].values[0]}")
    #                     st.write(f"- **Dinner**: {recommendations['Dinner'].values[0]}")
    #                     st.write(f"- **Detox Drinks**: {recommendations['Detox Drinks'].values[0]}")
    #                     st.write(f"- **Skincare Recommendations**: {recommendations['Skincare Recommendations'].values[0]}")
    #                     st.write(f"- **Home Remedies**: {recommendations['Home Remedies'].values[0]}")
    #         else:
    #             st.error("Unable to predict the acne type. Please try with a different image.")

    # if st.button("Back"):
    #     st.markdown("""
    #         <meta http-equiv="refresh" content="0;URL='http://localhost:5000'" />
    #     """, unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()
