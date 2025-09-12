#CKD Detection System

A web-based application for predicting Chronic Kidney Disease (CKD) using machine learning. This project integrates data preprocessing, model training, evaluation, and a user-friendly interface for real-time predictions.

#Project Structure
FINAL/ ├── app.py                          # Main application file ├── dataset/                        # Raw or processed datasets ├── final/ │   ├── ckd_model.pkl               # Trained ML model │   └── label_encoders.pkl          # Encoders for categorical features ├── src/ │   ├── preprocess.py               # Data preprocessing logic │   ├── training.py                 # Model training script │   └── evaluation.py               # Model evaluation metrics ├── static/ │   ├── css/ │   │   └── style.css               # Web styling │   └── js/ │       └── script.js               # Client-side scripting ├── templates/ │   └── index.html                  # Web interface template └── preprocessed_final_ckd.csv     # Preprocessed datase

#Features

- Predict CKD risk based on medical inputs
- Multi-language support (English, Kannada, Hindi)
- Downloadable prediction report (PDF)
- Responsive UI with animated background
- Model evaluation and training scripts included

#Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask
- **ML**: scikit-learn, pandas, numpy
- **PDF Generation**: ReportLab

#Model Details

- **Algorithm**: Random Forest
- **Training Data**: `preprocessed_final_ckd.csv`
- **Evaluation**: Accuracy, Precision, Recall, F1 Score (see `evaluation.py`)











