import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load your trained model (adjust path if needed)
def load_model():
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'ckd_model.pkl')
    model = joblib.load(model_path)
    return model

# Define the list of feature names your model expects (same as training)
FEATURES = [
    'age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr',
    'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn',
    'dm', 'cad', 'appet', 'pe', 'ane'
]

# Helper to get user inputs for each feature
def get_user_inputs():
    st.sidebar.header('Enter Patient Clinical Data')

    data = {}
    data['age'] = st.sidebar.number_input('Age', min_value=1, max_value=120, value=50)
    data['bp'] = st.sidebar.number_input('Blood Pressure', value=80)
    data['sg'] = st.sidebar.selectbox('Specific Gravity', options=[1.005, 1.010, 1.015, 1.020, 1.025])
    data['al'] = st.sidebar.selectbox('Albumin', options=[0, 1, 2, 3, 4, 5])
    data['su'] = st.sidebar.selectbox('Sugar', options=[0, 1, 2, 3, 4, 5])
    
    # For categorical features originally encoded as numbers, provide options:
    # For binary/categorical features with label encoding mapping known,
    # you can either ask raw input or map options to encoded values.
    # For simplicity, assume model expects numeric after encoding
    
    # Assuming these categorical features encoded as 0/1:
    data['rbc'] = st.sidebar.selectbox('Red Blood Cells (0=normal,1=abnormal)', options=[0,1])
    data['pc'] = st.sidebar.selectbox('Pus Cell (0=normal,1=abnormal)', options=[0,1])
    data['pcc'] = st.sidebar.selectbox('Pus Cell Clumps (0=no,1=yes)', options=[0,1])
    data['ba'] = st.sidebar.selectbox('Bacteria (0=no,1=yes)', options=[0,1])
    
    data['bgr'] = st.sidebar.number_input('Blood Glucose Random', value=100)
    data['bu'] = st.sidebar.number_input('Blood Urea', value=40)
    data['sc'] = st.sidebar.number_input('Serum Creatinine', value=1.0)
    data['sod'] = st.sidebar.number_input('Sodium', value=135)
    data['pot'] = st.sidebar.number_input('Potassium', value=4.5)
    data['hemo'] = st.sidebar.number_input('Hemoglobin', value=15.0)
    data['pcv'] = st.sidebar.number_input('Packed Cell Volume', value=40)
    data['wc'] = st.sidebar.number_input('White Blood Cell Count', value=8000)
    data['rc'] = st.sidebar.number_input('Red Blood Cell Count', value=4.5)
    
    # Binary encoded as 0 or 1 or similar:
    data['htn'] = st.sidebar.selectbox('Hypertension (0=no,1=yes)', [0,1])
    data['dm'] = st.sidebar.selectbox('Diabetes Mellitus (0=no,1=yes)', [0,1])
    data['cad'] = st.sidebar.selectbox('Coronary Artery Disease (0=no,1=yes)', [0,1])
    data['appet'] = st.sidebar.selectbox('Appetite (0=poor,1=good)', [0,1])
    data['pe'] = st.sidebar.selectbox('Pedal Edema (0=no,1=yes)', [0,1])
    data['ane'] = st.sidebar.selectbox('Anemia (0=no,1=yes)', [0,1])
    
    return pd.DataFrame([data])

def main():
    st.title("Chronic Kidney Disease (CKD) Prediction")

    model = load_model()

    user_input_df = get_user_inputs()

    st.subheader("Entered Patient Data")
    st.write(user_input_df)

    if st.button('Predict CKD'):
        # Run model prediction
        pred = model.predict(user_input_df)
        pred_proba = model.predict_proba(user_input_df)

        if pred[0] == 0:
            result = "No Chronic Kidney Disease"
        elif pred[0] == 1:
            result = "Mild Chronic Kidney Disease"
        else:
            result = "Severe Chronic Kidney Disease"

        st.subheader("Prediction Result")
        st.write(f"Model prediction: **{result}**")
        st.write(f"Prediction probabilities: {pred_proba}")

if __name__ == "__main__":
    main()
