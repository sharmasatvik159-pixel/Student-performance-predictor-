import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

def train_and_save_model():
    data_path = 'data/student_data.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run generate_data.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Features and Target
    X = df.drop('Final_Score', axis=1)
    y = df['Final_Score']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing
    numeric_features = ['Study_Hours', 'Attendance', 'Previous_Score']
    categorical_features = ['Parental_Education', 'Test_Preparation']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    # Create Pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Train model
    print("Training model...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate model
    score = model_pipeline.score(X_test, y_test)
    print(f"Model R^2 Score on test set: {score:.4f}")
    
    # Save model
    os.makedirs('model', exist_ok=True)
    joblib.dump(model_pipeline, 'model/model.joblib')
    print("Model saved to model/model.joblib")

if __name__ == '__main__':
    train_and_save_model()
