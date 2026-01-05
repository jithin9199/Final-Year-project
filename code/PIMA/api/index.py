from flask import Flask, request, jsonify
import joblib
import os
import sys

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), '../artifacts/final_model.joblib')
model = joblib.load(model_path)

@app.route('/')
def home():
    return jsonify({
        "message": "PIMA Diabetes Prediction API",
        "status": "running",
        "endpoint": "/predict"
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Expected features for PIMA diabetes prediction
        required_features = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                           'insulin', 'bmi', 'diabetes_pedigree', 'age']
        
        # Validate input
        if not all(feature in data for feature in required_features):
            return jsonify({
                "error": "Missing required features",
                "required": required_features
            }), 400
        
        # Prepare input data
        features = [[
            data['pregnancies'],
            data['glucose'],
            data['blood_pressure'],
            data['skin_thickness'],
            data['insulin'],
            data['bmi'],
            data['diabetes_pedigree'],
            data['age']
        ]]
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        return jsonify({
            "prediction": int(prediction),
            "probability": {
                "no_diabetes": float(probability[0]),
                "diabetes": float(probability[1])
            },
            "message": "Diabetes detected" if prediction == 1 else "No diabetes detected"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True)
