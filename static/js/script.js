// Language translations
const translations = {
    en: {
        'main-title': 'CKD Detection System',
        'subtitle': 'Advanced Chronic Kidney Disease Prediction',
        'label-sc': 'Serum Creatinine (mg/dL)',
        'label-hemo': 'Hemoglobin (g/dL)',
        'label-al': 'Albumin Level',
        'label-sg': 'Specific Gravity',
        'label-pcv': 'Packed Cell Volume (%)',
        'label-rbcc': 'Red Blood Cell Count (millions/μL)',
        'label-dm': 'Diabetes Mellitus',
        'label-htn': 'Hypertension',
        'dm-no': 'No',
        'dm-yes': 'Yes',
        'htn-no': 'No',
        'htn-yes': 'Yes',
        'btn-text': 'Predict CKD Risk',
        'result-title': 'Prediction Result',
        'download-btn': 'Download Report'
    },
    kn: {
        'main-title': 'CKD ಪತ್ತೆ ವ್ಯವಸ್ಥೆ',
        'subtitle': 'ಸುಧಾರಿತ ದೀರ್ಘಕಾಲಿಕ ಮೂತ್ರಪಿಂಡ ರೋಗ ಮುನ್ಸೂಚನೆ',
        'label-sc': 'ಸೀರಮ್ ಕ್ರಿಯೇಟಿನಿನ್ (mg/dL)',
        'label-hemo': 'ಹಿಮೋಗ್ಲೋಬಿನ್ (g/dL)',
        'label-al': 'ಅಲ್ಬುಮಿನ್ ಮಟ್ಟ',
        'label-sg': 'ವಿಶಿಷ್ಟ ಗುರುತ್ವ',
        'label-pcv': 'ಪ್ಯಾಕ್ಡ್ ಸೆಲ್ ವಾಲ್ಯೂಮ್ (%)',
        'label-rbcc': 'ಕೆಂಪು ರಕ್ತ ಕಣಗಳ ಸಂಖ್ಯೆ',
        'label-dm': 'ಮಧುಮೇಹ',
        'label-htn': 'ಅಧಿಕ ರಕ್ತದೊತ್ತಡ',
        'dm-no': 'ಇಲ್ಲ',
        'dm-yes': 'ಹೌದು',
        'htn-no': 'ಇಲ್ಲ',
        'htn-yes': 'ಹೌದು',
        'btn-text': 'CKD ಅಪಾಯ ಮುನ್ಸೂಚನೆ',
        'result-title': 'ಮುನ್ಸೂಚನೆ ಫಲಿತಾಂಶ',
        'download-btn': 'ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ'
    },
    hi: {
        'main-title': 'CKD डिटेक्शन सिस्टम',
        'subtitle': 'उन्नत क्रॉनिक किडनी रोग पूर्वानुमान',
        'label-sc': 'सीरम क्रिएटिनिन (mg/dL)',
        'label-hemo': 'हीमोग्लोबिन (g/dL)',
        'label-al': 'एल्ब्यूमिन स्तर',
        'label-sg': 'विशिष्ट गुरुत्व',
        'label-pcv': 'पैक्ड सेल वॉल्यूम (%)',
        'label-rbcc': 'लाल रक्त कोशिका गिनती',
        'label-dm': 'मधुमेह',
        'label-htn': 'उच्च रक्तचाप',
        'dm-no': 'नहीं',
        'dm-yes': 'हाँ',
        'htn-no': 'नहीं',
        'htn-yes': 'हाँ',
        'btn-text': 'CKD जोखिम पूर्वानुमान',
        'result-title': 'पूर्वानुमान परिणाम',
        'download-btn': 'रिपोर्ट डाउनलोड करें'
    }
};

let currentLanguage = 'en';
let lastPrediction = null;

// Create floating particles
function createParticles() {
    const bgAnimation = document.querySelector('.bg-animation');
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 6) + 's';
        bgAnimation.appendChild(particle);
    }
}

// Language switching
function setLanguage(lang) {
    currentLanguage = lang;
    
    // Update active button
    document.querySelectorAll('.language-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[onclick="setLanguage('${lang}')"]`).classList.add('active');
    
    // Update text content
    const translation = translations[lang];
    Object.keys(translation).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            if (element.tagName === 'OPTION') {
                element.textContent = translation[key];
            } else {
                element.textContent = translation[key];
            }
        }
    });
}

// Form submission
document.getElementById('ckd-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    
    // Show loading state
    const predictBtn = document.getElementById('predict-btn');
    const originalText = predictBtn.innerHTML;
    predictBtn.innerHTML = '<div class="spinner" style="display: inline-block; width: 20px; height: 20px; margin-right: 10px;"></div>Processing...';
    predictBtn.disabled = true;
    
    try {
        // Send data to Flask backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const result = await response.json();
        lastPrediction = result;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing your request. Please try again.');
    } finally {
        // Restore button state
        predictBtn.innerHTML = originalText;
        predictBtn.disabled = false;
    }
});

// Display results
function displayResults(result) {
    const resultContainer = document.getElementById('result-container');
    const resultContent = document.getElementById('result-content');
    
    const riskClass = result.prediction === 'High Risk' ? 'risk-high' : 'risk-low';
    
    let riskFactorsHtml = '';
    if (result.riskFactors && result.riskFactors.length > 0) {
        riskFactorsHtml = `<p><strong>Risk Factors:</strong> ${result.riskFactors.join(', ')}</p>`;
    }
    
    resultContent.innerHTML = `
        <h3 class="${riskClass}">${result.prediction}</h3>
        <p><strong>Probability:</strong> ${result.probability.toFixed(1)}%</p>
        ${riskFactorsHtml}
        <p><strong>Confidence:</strong> ${result.confidence || 'N/A'}</p>
        <br>
        <p><em>Note: This is a prediction model. Please consult with a healthcare professional for proper diagnosis.</em></p>
    `;
    
    resultContainer.style.display = 'block';
    
    // Scroll to results
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Download report function
async function downloadReport() {
    if (!lastPrediction) return;
    
    try {
        const response = await fetch('/download_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(lastPrediction)
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `CKD_Report_${new Date().getTime()}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error('Error:', error);
        
        // Fallback to text download
        const reportContent = generateTextReport(lastPrediction);
        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `CKD_Report_${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Generate text report
function generateTextReport(prediction) {
    return `
CKD DETECTION REPORT
====================
Date: ${new Date().toLocaleDateString()}
Time: ${new Date().toLocaleTimeString()}

PATIENT DATA:
-------------
Serum Creatinine: ${prediction.formData.sc} mg/dL
Hemoglobin: ${prediction.formData.hemo} g/dL
Albumin Level: ${prediction.formData.al}
Specific Gravity: ${prediction.formData.sg}
Packed Cell Volume: ${prediction.formData.pcv}%
Red Blood Cell Count: ${prediction.formData.rbcc} millions/μL
Diabetes Mellitus: ${prediction.formData.dm === '1' ? 'Yes' : 'No'}
Hypertension: ${prediction.formData.htn === '1' ? 'Yes' : 'No'}

PREDICTION RESULTS:
------------------
Risk Assessment: ${prediction.prediction}
Probability: ${prediction.probability.toFixed(1)}%
Risk Factors: ${prediction.riskFactors && prediction.riskFactors.length > 0 ? prediction.riskFactors.join(', ') : 'None identified'}
Confidence: ${prediction.confidence || 'N/A'}

DISCLAIMER:
-----------
This report is generated by an AI prediction model and should not be used as a substitute for professional medical advice. Please consult with a qualified healthcare provider for proper diagnosis and treatment.

Generated by CKD Detection System
    `;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    createParticles();
    setLanguage('en');
});