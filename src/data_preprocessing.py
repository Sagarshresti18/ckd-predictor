import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_data():
    """
    Load the Chronic Kidney Disease dataset CSV file from the data folder,
    skipping first metadata line if present, removing extra unwanted columns,
    and assigning correct column names.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root 'lzy'
    filepath = os.path.join(base_dir, 'data', 'chronic_kidney_disease.csv')
    
    # Read CSV, skip first metadata line usually present in UCI CKD dataset
    df = pd.read_csv(filepath, skiprows=1)
    
    # Drop extra first column if it's index or unwanted (adjust if needed)
    # (Your earlier load showed 26 columns but only 25 column names - usually the first is index)
    df = df.iloc[:, 1:]  # drop first column
    
    # Define correct column names for 25 columns
    column_names = [
        'age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu',
        'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad',
        'appet', 'pe', 'ane', 'class'
    ]
    df.columns = column_names
    
    return df

def preprocess_data(df):
    """
    Preprocess CKD dataset:
    - Fill missing numeric values with median
    - Forward fill missing categorical values
    - Encode categorical columns to numeric labels
    - Scale numerical features
    """
    # Fill numeric missing values with median
    df.fillna(df.median(numeric_only=True), inplace=True)
    # Forward fill other (categorical) missing values
    df.ffill(inplace=True)

    # Encode categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    # Scale features except target 'class'
    features = df.columns.difference(['class'])
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])

    return df

if __name__ == "__main__":
    df = load_data()
    df = preprocess_data(df)
    print(df.head())
    print(df.info())
