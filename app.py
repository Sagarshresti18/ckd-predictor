from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import joblib
import os
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Load trained model
try:
    model = joblib.load("final/ckd_model.pkl")
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Warning: Model file not found. Using fallback prediction method.")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class CKDPredictor:
    def __init__(self):
        """Initialize fallback predictor with medical knowledge"""
        # Define normal ranges for parameters
        self.normal_ranges = {
            'sc': (0.6, 1.3),      # Serum Creatinine (mg/dL)
            'hemo': (12.0, 17.0),   # Hemoglobin (g/dL) 
            'sg': (1.010, 1.025),   # Specific Gravity
            'pcv': (36.0, 48.0),    # Packed Cell Volume (%)
            'rbcc': (4.2, 5.4),     # Red Blood Cell Count (millions/μL)
        }
        
        # Risk factor weights
        self.risk_weights = {
            'sc_high': 0.25,     # High serum creatinine
            'hemo_low': 0.20,    # Low hemoglobin
            'sg_abnormal': 0.15, # Abnormal specific gravity
            'pcv_low': 0.15,     # Low packed cell volume
            'rbcc_low': 0.10,    # Low red blood cell count
            'albumin_high': 0.20, # High albumin (proteinuria)
            'diabetes': 0.15,     # Diabetes mellitus
            'hypertension': 0.10  # Hypertension
        }
    
    def extract_risk_factors(self, data):
        """Extract risk factors from patient data"""
        risk_factors = []
        risk_score = 0.0
        
        # Convert inputs to appropriate types
        sc = float(data[0])    # Serum Creatinine
        hemo = float(data[1])  # Hemoglobin
        al = int(data[2])      # Albumin Level
        sg = float(data[3])    # Specific Gravity
        pcv = float(data[4])   # Packed Cell Volume
        rbcc = float(data[5])  # Red Blood Cell Count
        dm = int(data[6])      # Diabetes Mellitus
        htn = int(data[7])     # Hypertension
        
        # Check serum creatinine (high indicates kidney dysfunction)
        if sc > self.normal_ranges['sc'][1]:
            risk_factors.append("Elevated Serum Creatinine")
            if sc > 3.0:
                risk_score += self.risk_weights['sc_high'] * 2
            else:
                risk_score += self.risk_weights['sc_high']
        
        # Check hemoglobin (low indicates anemia)
        if hemo < self.normal_ranges['hemo'][0]:
            risk_factors.append("Low Hemoglobin (Anemia)")
            risk_score += self.risk_weights['hemo_low']
        
        # Check specific gravity
        if sg < self.normal_ranges['sg'][0] or sg > self.normal_ranges['sg'][1]:
            risk_factors.append("Abnormal Urine Specific Gravity")
            risk_score += self.risk_weights['sg_abnormal']
        
        # Check packed cell volume
        if pcv < self.normal_ranges['pcv'][0]:
            risk_factors.append("Low Packed Cell Volume")
            risk_score += self.risk_weights['pcv_low']
        
        # Check red blood cell count
        if rbcc < self.normal_ranges['rbcc'][0]:
            risk_factors.append("Low Red Blood Cell Count")
            risk_score += self.risk_weights['rbcc_low']
        
        # Check albumin level
        if al > 0:
            albumin_levels = ["Trace", "1+", "2+", "3+", "4+", "5+"]
            if al <= len(albumin_levels):
                risk_factors.append(f"Proteinuria ({albumin_levels[al-1]})")
                risk_score += self.risk_weights['albumin_high'] * (al / 5.0)
        
        # Check diabetes mellitus
        if dm == 1:
            risk_factors.append("Diabetes Mellitus")
            risk_score += self.risk_weights['diabetes']
        
        # Check hypertension
        if htn == 1:
            risk_factors.append("Hypertension")
            risk_score += self.risk_weights['hypertension']
        
        return risk_factors, risk_score
    
    def predict_fallback(self, input_data):
        """Fallback prediction when model is not available"""
        risk_factors, risk_score = self.extract_risk_factors(input_data[0])
        
        # Calculate probability
        probability = min(risk_score * 100 / 1.3, 95)
        
        # Determine prediction
        if probability >= 60:
            prediction = "High Risk"
            confidence = "High"
        elif probability >= 30:
            prediction = "Moderate Risk" 
            confidence = "Medium"
        else:
            prediction = "Low Risk"
            confidence = "Medium"
        
        # Special case for very high creatinine
        if input_data[0][0] > 4.0:  # sc > 4.0
            prediction = "High Risk"
            probability = max(probability, 85)
            confidence = "High"
        
        return prediction, probability, risk_factors, confidence

# Initialize fallback predictor
fallback_predictor = CKDPredictor()

# Input preprocessing function
def preprocess_input(form_data):
    """Preprocess input data for model prediction"""
    try:
        sc = float(form_data['sc'])
        hemo = float(form_data['hemo'])
        al = int(form_data['al'])
        sg = float(form_data['sg'])
        pcv = float(form_data['pcv'])
        rbcc = float(form_data['rbcc'])
        
        # Handle different input formats for dm and htn
        if isinstance(form_data['dm'], str):
            dm = 1 if form_data['dm'].lower() in ['yes', '1', 'true'] else 0
        else:
            dm = int(form_data['dm'])
            
        if isinstance(form_data['htn'], str):
            htn = 1 if form_data['htn'].lower() in ['yes', '1', 'true'] else 0
        else:
            htn = int(form_data['htn'])
            
    except (ValueError, KeyError) as e:
        return None, f"Invalid input: {str(e)}"

    # Validate ranges
    if not (0.1 <= sc <= 20.0):
        return None, "Serum Creatinine must be between 0.1 and 20.0 mg/dL"
    if not (2.0 <= hemo <= 20.0):
        return None, "Hemoglobin must be between 2.0 and 20.0 g/dL"
    if not (1.000 <= sg <= 1.040):
        return None, "Specific Gravity must be between 1.000 and 1.040"
    if not (10.0 <= pcv <= 60.0):
        return None, "Packed Cell Volume must be between 10 and 60%"
    if not (1.0 <= rbcc <= 10.0):
        return None, "Red Blood Cell Count must be between 1.0 and 10.0 millions/μL"

    return np.array([[sc, hemo, al, sg, pcv, rbcc, dm, htn]]), None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests - supports both form and JSON data"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            form_data = request.get_json()
        else:
            form_data = request.form.to_dict()
        
        # Validate required fields
        required_fields = ['sc', 'hemo', 'al', 'sg', 'pcv', 'rbcc', 'dm', 'htn']
        for field in required_fields:
            if field not in form_data or form_data[field] == '':
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'success': False
                }), 400
        
        # Preprocess input
        input_data, error = preprocess_input(form_data)
        if input_data is None:
            return jsonify({
                'error': error,
                'success': False
            }), 400
        
        # Make prediction
        if model is not None:
            try:
                # Use trained model
                prediction_raw = model.predict(input_data)[0]
                
                # Get probability if available
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(input_data)[0]
                    probability = proba[1] * 100  # Probability of CKD (class 1)
                else:
                    probability = 85.0 if prediction_raw == 1 else 15.0
                
                # Convert numerical prediction to text
                if prediction_raw == 1:
                    prediction = "High Risk"
                    confidence = "High"
                else:
                    prediction = "Low Risk" 
                    confidence = "High"
                
                # Extract risk factors for explanation
                risk_factors, _ = fallback_predictor.extract_risk_factors(input_data[0])
                
            except Exception as e:
                print(f"Model prediction error: {e}")
                # Fallback to rule-based prediction
                prediction, probability, risk_factors, confidence = fallback_predictor.predict_fallback(input_data)
        else:
            # Use fallback predictor
            prediction, probability, risk_factors, confidence = fallback_predictor.predict_fallback(input_data)
        
        # Prepare response
        result = {
            'prediction': prediction,
            'probability': probability,
            'riskFactors': risk_factors,
            'confidence': confidence,
            'formData': form_data,
            'success': True
        }
        
        # Handle non-JSON requests (original form submission)
        if not request.is_json:
            if prediction == "High Risk":
                result_text = "⚠️ CKD Detected. Please consult a healthcare professional for further evaluation."
            else:
                result_text = "✅ No CKD detected. Keep monitoring and stay healthy."
            return render_template('result.html', prediction=result_text)
        
        return jsonify(result)
        
    except Exception as e:
        error_msg = f'An error occurred during prediction: {str(e)}'
        print(error_msg)
        
        if request.is_json:
            return jsonify({
                'error': error_msg,
                'success': False
            }), 500
        else:
            return render_template('result.html', prediction="An error occurred. Please try again.")

@app.route('/download_report', methods=['POST'])
def download_report():
    """Generate and download PDF report"""
    try:
        # Get prediction data from request
        data = request.get_json()
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph("CKD DETECTION REPORT", title_style))
        story.append(Spacer(1, 20))
        
        # Date and time
        current_time = datetime.now()
        story.append(Paragraph(f"<b>Generated:</b> {current_time.strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Patient Data Section
        story.append(Paragraph("PATIENT DATA", heading_style))
        
        patient_data = [
            ['Parameter', 'Value', 'Normal Range'],
            ['Serum Creatinine', f"{data['formData']['sc']} mg/dL", '0.6 - 1.3 mg/dL'],
            ['Hemoglobin', f"{data['formData']['hemo']} g/dL", '12.0 - 17.0 g/dL'],
            ['Albumin Level', data['formData']['al'], '0 (Normal)'],
            ['Specific Gravity', data['formData']['sg'], '1.010 - 1.025'],
            ['Packed Cell Volume', f"{data['formData']['pcv']}%", '36 - 48%'],
            ['Red Blood Cell Count', f"{data['formData']['rbcc']} millions/μL", '4.2 - 5.4 millions/μL'],
            ['Diabetes Mellitus', 'Yes' if str(data['formData']['dm']) == '1' else 'No', 'No'],
            ['Hypertension', 'Yes' if str(data['formData']['htn']) == '1' else 'No', 'No']
        ]
        
        patient_table = Table(patient_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # Prediction Results Section
        story.append(Paragraph("PREDICTION RESULTS", heading_style))
        
        # Risk assessment with color coding
        risk_color = colors.red if data['prediction'] == 'High Risk' else colors.orange if 'Moderate' in data['prediction'] else colors.green
        story.append(Paragraph(f"<b>Risk Assessment:</b> <font color='{risk_color.hexval()}'>{data['prediction']}</font>", styles['Normal']))
        story.append(Paragraph(f"<b>Probability:</b> {data['probability']:.1f}%", styles['Normal']))
        story.append(Paragraph(f"<b>Confidence:</b> {data.get('confidence', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Risk factors
        if data.get('riskFactors') and len(data['riskFactors']) > 0:
            story.append(Paragraph("<b>Identified Risk Factors:</b>", styles['Normal']))
            for factor in data['riskFactors']:
                story.append(Paragraph(f"• {factor}", styles['Normal']))
        else:
            story.append(Paragraph("<b>Risk Factors:</b> None identified", styles['Normal']))
        
        story.append(Spacer(1, 30))
        
        # Model information
        model_info = "Machine Learning Model" if model is not None else "Rule-based Clinical Assessment"
        story.append(Paragraph(f"<b>Analysis Method:</b> {model_info}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Disclaimer
        story.append(Paragraph("IMPORTANT DISCLAIMER", heading_style))
        disclaimer_text = """
        This AI-generated report is for informational purposes only and not a substitute for professional medical advice.
        Always consult a qualified healthcare provider with any medical concerns.
        """
        story.append(Paragraph(disclaimer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'CKD_Report_{current_time.strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {e}")
        return jsonify({
            'error': f'Failed to generate report: {str(e)}',
            'success': False
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True)
