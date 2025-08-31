import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report

def evaluate(input_csv, model_path):
    data = pd.read_csv(input_csv)
    X = data.drop('prediction', axis=1)  # Change 'class' if your target column is different
    y = data['prediction']
    clf = joblib.load(model_path)
    y_pred = clf.predict(X)
    print("Accuracy:", accuracy_score(y, y_pred))
    print(classification_report(y, y_pred))

if __name__ == "__main__":
    evaluate(
        input_csv='preprocessed_ckd.csv',
        model_path='models/ckd_model.pkl'
    )