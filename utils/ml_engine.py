import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/insurance_model.pkl')

def load_prediction_model():
    """Loads the pre-trained ML model strictly from the file."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    # Strictly load the model you provided
    model = joblib.load(MODEL_PATH)
    return model

def predict_insurance_charges(input_data):
    """
    input_data: dict containing features
    Returns the predicted charge.
    """
    model = load_prediction_model()
    
    df = pd.DataFrame([input_data])
    
    # We must convert strings into numbers manually since you didn't save the LabelEncoders 
    # when training on Colab. (LabelEncoder assigns alphabetically).
    df["sex"] = df["sex"].map({"male": 1, "female": 0})
    df["smoker"] = df["smoker"].map({"yes": 1, "no": 0})
    df["region"] = df["region"].map({"northeast": 0, "northwest": 1, "southeast": 2, "southwest": 3})
    
    # Make prediction strictly using your model
    prediction = model.predict(df)
    return float(prediction[0])

