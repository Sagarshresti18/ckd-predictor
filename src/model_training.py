import os
import sys
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Add src directory to path for imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from data_preprocessing import load_data, preprocess_data

def train_model():
    # Load and preprocess data
    df = load_data()
    df = preprocess_data(df)

    # Separate features and target
    X = df.drop('class', axis=1)
    y = df['class']

    # Split to train/test sets with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # Apply SMOTE to balance classes in training set
    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    # Define hyperparameter grid for tuning Random Forest
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
    }

    # Initialize Random Forest with class weight balancing
    rf = RandomForestClassifier(random_state=42, class_weight='balanced')

    # Grid Search with 5-fold cross-validation
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )

    # Fit Grid Search on resampled training data
    grid_search.fit(X_train_res, y_train_res)
    best_model = grid_search.best_estimator_

    print(f"Best hyperparameters: {grid_search.best_params_}")

    # Evaluate the best model on the test set
    y_pred = best_model.predict(X_test)
    print("\nClassification Report on Test Set:\n")
    print(classification_report(y_test, y_pred))

    # Save the trained model to models/ directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(project_root, 'models')
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, 'ckd_model.pkl')
    joblib.dump(best_model, model_path)

    print(f"\nModel saved successfully at:\n{model_path}")

if __name__ == "__main__":
    train_model()
