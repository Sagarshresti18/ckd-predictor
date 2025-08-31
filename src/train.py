import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train(input_csv, model_path):
    data = pd.read_csv(input_csv)
    X = data.drop('prediction', axis=1)  # Change 'class' if your target column is different
    y = data['prediction']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(clf, model_path)
    return X_test, y_test

if __name__ == "__main__":
    train(
        input_csv='preprocessed_ckd.csv',
        model_path='models/ckd_model.pkl'
    )