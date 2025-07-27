import os
import sys
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from data_preprocessing import load_data, preprocess_data

# Load data and model
df = preprocess_data(load_data())
X = df.drop('class', axis=1)
y = df['class']

model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'ckd_model.pkl')
clf = joblib.load(model_path)

y_pred = clf.predict(X)

# Plot confusion matrix
cm = confusion_matrix(y, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Confusion Matrix - CKD Model")
plt.show()
