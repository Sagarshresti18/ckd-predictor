# Chronic Kidney Disease (CKD) Prediction

## Project Overview

This project predicts Chronic Kidney Disease (CKD) using machine learning on clinical and laboratory data of patients. It implements data preprocessing, handles class imbalance with SMOTE, employs Random Forest (and optionally XGBoost) for model training with hyperparameter tuning, and evaluates performance using classification reports and confusion matrices. An interactive Streamlit app serves as a user-friendly interface for real-time CKD risk prediction.

Early prediction of CKD is crucial for timely intervention and improving patient outcomes. This repository provides a modular, reproducible, and extensible framework for CKD detection using ML.

## Features

- Data loading and cleaning (imputation and encoding)
- Handling class imbalance with SMOTE
- Model training with Random Forest and hyperparameter tuning
- Optional integration of XGBoost classifier
- Detailed evaluation metrics including confusion matrix visualization
- Streamlit-based interactive web app for input and prediction
- Modular code structure for easy extension

## Installation
1. Clone the repository:
git clone https://github.com/Sagarshresti18/ckd-predictor.git
cd ckd-predictor
2. (Optional) Create a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
3. Install required dependencies:
pip install -r requirements.txt

*Make sure `requirements.txt` is updated with packages like pandas, scikit-learn, imbalanced-learn, xgboost, streamlit, etc.*

## Usage

### Train and evaluate model
Run your main script or notebook to preprocess data, train your model, and evaluate metrics.
python train.py

*(Adjust command based on your project’s actual script)*
### Run the Streamlit app
To launch the interactive app for CKD prediction:
streamlit run app.py
Then open the URL shown (usually http://localhost:8501) in your browser.

## Project Structure
/ckd-prediction
│
├── data/ # Dataset files (if included)
├── models/ # Saved trained models
├── notebooks/ # Jupyter notebooks (if any)
├── src/ # Source code files
├── app.py # Streamlit web app
├── requirements.txt # Required Python packages
├── README.md # Project documentation
└── .gitignore # Git ignore rules






