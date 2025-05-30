FACEMAP: AI-Powered Skin Type and Acne Analysis in Real-Time


FaceMap is an AI-driven skincare analysis web application designed to perform real-time detection of skin types and acne severity using facial image processing. It leverages machine learning models and integrates modern dermatology with traditional **Ayurvedic principles** to provide personalized skincare insights and recommendations.

Key Features
- Real-Time Image-Based Skin Analysis  
- Age and Gender Detection using pretrained ML models  
- Skin Type Classification Oily, Dry, Combination, Sensitive  
- Acne Detection & Grading with severity and type (e.g., blackheads, cystic)  
- Ayurvedic Acne Typing – Vataj, Pittaj, Kaphaj, and combinations (e.g., Vatta-Pitta)  
- Personalized Recommendations – Diet (breakfast, lunch, dinner), skincare, detox drinks, home remedies  
- PDF Report Generation with diagnostic results and suggestions  
- Progress Tracking using historical analysis data  


Tech Stack
- Frontend: HTML, CSS, JavaScript  
- Backend: Python, Flask  
- ML Frameworks: TensorFlow/Keras, OpenCV  
- Pretrained Models:Caffe models (for age/gender detection)  
- Database: SQLite (local), Firebase (cloud-based backup)  
- ML Architectures: CNN (VGG, ResNet, MobileNet), YOLO (acne detection)


Image Processing Pipeline
- Image Capture– Upload or capture real-time image
- Age & Gender Prediction – Using pretrained models
- Skin Type & Acne Detection – CNN-based classification
- Ayurvedic Typing – Classify acne as Vataj, Pittaj, Kaphaj or combinations
- Recommendations – Based on acne type and symptoms
- PDF Export – Personalized report generation


Symptom Images Directory
Images must be placed in a local directory and follow this naming convention:

| Acne Type          | Folder/File Prefix | Example Filename          |
|--------------------|--------------------|---------------------------|
| Pittaj             | `P`                | `P1.jpg`, `P2.jpg`, ...   |
| Kaphaj             | `K`                | `K1.jpg`, `K2.jpg`, ...   |
| Vattaj             | `V`                | `V1.jpg`, `V2.jpg`, ...   |
| Pittaj-Kaphaj      | `PK`               | `PK1.jpg`, `PK2.jpg`, ... |
| Vattaj-Pittaj      | `VP`               | `VP1.jpg`, `VP2.jpg`, ... |
| Vattaj-Kaphaj      | `VK`               | `VK1.jpg`, `VK2.jpg`, ... |

Set the image path in your Python code (e.g., in `symptom_based.py`): python
image_folder_path = "path/to/your/(folder in which all the images are saved)"

Datasets & Training
-Personalized datasets for skin type and acne classification
-Custom-labeled images for Ayurvedic acne classification
-Transfer learning on pretrained models 
-Real-time optimized model inference

Use Cases
-Personal Skincare Advisor
-Dermatology Pre-screening Tool
-Skin Health Research Aid
-Holistic Ayurvedic Skin Typing

Privacy Notice : Patient image data is not stored or shared. Only local analysis is performed unless explicitly configured otherwise. 

| File/Folder        | Description                        |
| ------------------ | ---------------------------------- |
| model.h5           | Trained model (via Git LFS)        |
| symptom_based.py   | Symptom-image-based analysis logic |
| models/            | All Caffe pretrained model files   |
| trial_images/      | Patient image folder (local only)  |
| requirements.txt   | Python dependencies                |
| templates/         | HTML pages                         |
| static/            | CSS, JavaScript, assets            |
| generate_pdf.py    | Report generation script           |


Model Files
> Note: The trained model `model.h5` is stored using Git LFS.  
Download it from the repo or clone with `git lfs clone`.





