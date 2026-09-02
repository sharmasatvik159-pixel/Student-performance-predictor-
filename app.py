from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the model
MODEL_PATH = 'model/model.joblib'
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}. Please train the model first.")

load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not trained yet.'}), 500
        
    try:
        data = request.json
        
        # Convert dictionary to DataFrame for the model
        df = pd.DataFrame([data])
        
        # Make prediction
        prediction = model.predict(df)[0]
        
        return jsonify({'prediction': round(prediction, 1)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Ensure model is re-loaded in case it was generated after startup
    load_model()
    app.run(debug=True, port=5000)
