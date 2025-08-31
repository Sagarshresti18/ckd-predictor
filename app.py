from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model and encoders
model = joblib.load('models/ckd_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect all 24 inputs from the form
    input_features = [
        int(request.form['age']),
        int(request.form['bp']),
        float(request.form['sg']),
        int(request.form['al']),
        int(request.form['su']),
        int(request.form['rbc']),
        int(request.form['pc']),
        int(request.form['pcc']),
        int(request.form['ba']),
        float(request.form['bgr']),
        int(request.form['bu']),  # Blood Urea - missing in original
        float(request.form['sc']),
        float(request.form['sod']),
        float(request.form['pot']),
        float(request.form['hemo']),
        float(request.form['pcv']),
        int(request.form['wc']),
        float(request.form['rc']),
        int(request.form['htn']),
        int(request.form['dm']),
        int(request.form['cad']),
        int(request.form['appet']),
        int(request.form['pe']),
        int(request.form['ane'])
    ]
    # Reshape for prediction
    input_array = np.array(input_features).reshape(1, -1)
    prediction = model.predict(input_array)[0]
    result = "CKD Detected" if prediction == 0 else "No CKD"
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)