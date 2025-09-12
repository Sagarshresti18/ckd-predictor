#CKD Detection System

A web-based application for predicting Chronic Kidney Disease (CKD) using machine learning. This project integrates data preprocessing, model training, evaluation, and a user-friendly interface for real-time predictions.

#Project Structure
CKD/ 
├── app.py                      # Main Flask application 
├── dataset/                    # Raw or processed datasets 
├── final/ 
   ├── ckd_model.pkl           # Trained ML model    
   └── label_encoders.pkl      # Encoders for categorical features 
├── src/ 
   ├── preprocess.py           # Data preprocessing logic    
   ├── training.py             # Model training script   
   └── evaluation.py           # Model evaluation metrics 
├── static/ 
   ├── css/style.css           # Styling for the web interface 
   └── js/script.js            # Client-side interactivity 
├── templates/ 
   └── index.html              # Main HTML page 
└── preprocessed_final_ckd.csv # Preprocessed dataset
└── requirements.txt

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


#Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CKD.git
   cd CKD

Create a virtual environment:
python -m venv venv
venv\Scripts\activate

Install required libraries:
pip install -r requirements.txt

Run the application:
python app.py





