import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def preprocess(input_csv, output_csv, encoder_path):
    data = pd.read_csv(input_csv)
    # Columns to encode ('class','prediction','rbc', etc.)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    le_dict = {}
    for col in categorical_cols:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        le_dict[col] = le
    data.to_csv(output_csv, index=False)
    os.makedirs(os.path.dirname(encoder_path), exist_ok=True)
    joblib.dump(le_dict, encoder_path)

if __name__ == "__main__":
    preprocess(
        input_csv='data/cleaned_combined_ckd.csv',
        output_csv='preprocessed_ckd.csv',
        encoder_path='models/label_encoders.pkl'
    )