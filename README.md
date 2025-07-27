Chronic Kidney Disease Prediction
Project Overview
This project implements a machine learning pipeline to predict Chronic Kidney Disease (CKD) based on clinical and laboratory features. It includes data preprocessing, model training using Random Forest with imbalance handling, evaluation, and a user interface for interactive predictions.

The goal is to assist in early CKD detection through an interpretable, accurate predictive model.

Dataset
Source: [Provide source, e.g., UCI Machine Learning Repository or your custom data]

Description: Contains clinical and laboratory features from patients, labeled with CKD diagnosis classes.

Number of samples: 427 (original), easily extendable by adding more rows to data/chronic_kidney_disease.csv.

Key features: age, blood pressure, specific gravity, albumin, sugar, red blood cells, pus cells, etc
lzy/
├── data/
│   └── chronic_kidney_disease.csv       # Raw dataset CSV
├── models/
│   └── ckd_model.pkl                     # Saved trained model file
├── notebooks/
│   └── exploration.ipynb                 # Exploratory Data Analysis & Visualization
├── src/
│   ├── data_preprocessing.py             # Loading and preprocessing dataset
│   ├── model_training.py                  # Model training & hyperparameter tuning
│   ├── model_evaluation.py                # Model evaluation & confusion matrix plotting
│   └── app.py                            # Streamlit app for CKD prediction
├── README.md                             # This file
└── requirements.txt                      # Python dependencies
