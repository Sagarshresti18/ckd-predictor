# Import necessary libraries
import pandas as pd                                # For data manipulation
from sklearn.model_selection import train_test_split  # For splitting data into training and testing sets
from sklearn.ensemble import RandomForestClassifier   # For building the classification model
import joblib                                       # For saving the trained model
import os                                           # For handling file paths and directories

def train_model(data_path, model_path):
    # Load the preprocessed dataset
    df = pd.read_csv(data_path)

    # Separate features (X) and target variable (y)
    X = df.drop(['class_encoded', 'class'], axis=1)  # Drop target columns to get feature set
    y = df['class_encoded']                          # Use encoded class labels as target

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y  # Stratify to maintain class distribution
    )

    # Initialize and train the Random Forest classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Ensure the directory for saving the model exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the trained model to the specified path
    joblib.dump(model, model_path)

# Execute the training function if the script is run directly
if __name__ == "__main__":
    train_model(
        data_path="preprocessed_final_ckd.csv",       # Path to the input dataset
        model_path="final/ckd_model.pkl"              # Path to save the trained model
    )
