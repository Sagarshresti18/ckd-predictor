# CKD Detection System

A web-based application for predicting Chronic Kidney Disease (CKD) using a machine learning model. This project includes data preprocessing, model training, and a user-friendly interface for real-time predictions.

## Features

-   **CKD Prediction:** Predicts the risk of CKD based on user-provided medical data.
-   **User-Friendly Interface:** A simple web interface for entering patient data.
-   **PDF Report Generation:** Generates a downloadable PDF report of the prediction results.
-   **Fallback Prediction:** Includes a rule-based fallback mechanism for predictions if the machine learning model is unavailable.

## Tech Stack

-   **Backend:** Flask
-   **Frontend:** HTML, CSS, JavaScript
-   **Machine Learning:** scikit-learn, pandas, numpy
-   **PDF Generation:** ReportLab

## Project Structure

```
.
├── app.py                      # Main Flask application
├── requirements.txt            # Project dependencies
├── dataset/
│   └── final.csv               # Raw dataset
├── final/
│   ├── ckd_model.pkl           # Trained machine learning model
│   └── label_encoders.pkl      # Saved label encoders
├── src/
│   ├── preprocess.py           # Data preprocessing script
│   ├── train.py                # Model training script
│   └── evaluation.py           # Model evaluation script
├── static/
│   ├── css/
│   └── js/
└── templates/
    └── index.html              # HTML template for the web interface
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ckd-detection-system.git
    cd ckd-detection-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the preprocessing and training scripts (optional, as the trained model is provided):**
    ```bash
    python src/preprocess.py
    python src/train.py
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1.  Enter the patient's medical data in the web interface.
2.  Click the "Predict" button to get the CKD risk prediction.
3.  Download the PDF report for a detailed summary of the results.

## Model Details

-   **Algorithm:** Random Forest Classifier
-   **Features:** Serum Creatinine, Hemoglobin, Albumin, Specific Gravity, Packed Cell Volume, Red Blood Cell Count, Diabetes Mellitus, Hypertension
-   **Training Data:** `preprocessed_final_ckd.csv`

## Scripts

-   `src/preprocess.py`: This script loads the raw data from `dataset/final.csv`, performs label encoding on categorical features, and saves the processed data and encoders.
-   `src/train.py`: This script trains a Random Forest model on the preprocessed data and saves the trained model to `final/ckd_model.pkl`.
-   `src/evaluation.py`: This script evaluates the trained model using various metrics and generates a classification report and confusion matrix.
