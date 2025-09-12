# Import necessary libraries
import pandas as pd                          # For reading and manipulating CSV data
from sklearn.preprocessing import LabelEncoder  # For encoding categorical variables
import joblib                                # For saving/loading Python objects
import os                                    # For file and directory operations

def preprocess(input_csv, output_csv, encoder_path):
    # Load the dataset from the input CSV file
    data = pd.read_csv(input_csv)

    # Identify categorical columns (excluding the target column 'class' if present)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    categorical_cols = [col for col in categorical_cols if col != 'class']  # Optional exclusion of target column

    # Initialize a dictionary to store label encoders for each categorical column
    le_dict = {}
    for col in categorical_cols:
        le = LabelEncoder()                          # Create a new LabelEncoder instance
        data[col] = le.fit_transform(data[col].astype(str))  # Encode the column and update the dataframe
        le_dict[col] = le                            # Store the encoder for future use

    # Save the processed data to the output CSV file
    data.to_csv(output_csv, index=False)

    # Ensure the directory for saving encoders exists
    encoder_dir = os.path.dirname(encoder_path)
    if encoder_dir:
        os.makedirs(encoder_dir, exist_ok=True)      # Create directory if it doesn't exist

    # Save the dictionary of label encoders to a file using joblib
    joblib.dump(le_dict, encoder_path)

# Run the preprocessing function if this script is executed directly
if __name__ == "__main__":
    preprocess(
        input_csv='dataset/final.csv',               # Path to the raw input dataset
        output_csv='preprocessed_final_ckd.csv',     # Path to save the processed dataset
        encoder_path='final/label_encoders.pkl'      # Path to save the label encoders
    )
