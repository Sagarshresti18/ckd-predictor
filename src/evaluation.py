# Import necessary libraries
import pandas as pd                # For data manipulation
import joblib                      # For loading the saved model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score  # For evaluation metrics

def evaluate_model(data_path, model_path):
    # Load the dataset from the given CSV file
    df = pd.read_csv(data_path)
    
    # Load the trained model from the specified path
    model = joblib.load(model_path)

    # Separate features (X) and target variable (y)
    X = df.drop(['class_encoded', 'class'], axis=1)  # Drop target columns to get feature set
    y = df['class_encoded']                          # Use encoded class labels as target

    # Make predictions using the loaded model
    y_pred = model.predict(X)

    # Print accuracy score
    print("Accuracy:", accuracy_score(y, y_pred))

    # Print confusion matrix to show prediction breakdown
    print("Confusion Matrix:")
    print(confusion_matrix(y, y_pred))

    # Print detailed classification report (precision, recall, f1-score)
    print("\nClassification Report:")
    print(classification_report(y, y_pred))

# Run the evaluation only if this script is executed directly
if __name__ == "__main__":
    evaluate_model(
        data_path="preprocessed_final_ckd.csv",      # Path to the preprocessed dataset
        model_path="final/ckd_model.pkl"             # Path to the saved model
    )
