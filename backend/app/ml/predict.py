import joblib
import numpy as np
import os

models = {}

def load_models():
    global models
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    for comp in ["brakes", "chain", "tires"]:
        model_path = os.path.join(model_dir, f"{comp}_model.joblib")
        if os.path.exists(model_path):
            models[comp] = joblib.load(model_path)
    print("✅ Models loaded:", list(models.keys()))

def predict_bike(bike_id: int):
    np.random.seed(bike_id)
    features = np.random.rand(7).reshape(1, -1)
    probs = {}
    for comp, model in models.items():
        try:
            probs[comp] = float(model.predict_proba(features)[0, 1])
        except:
            probs[comp] = float(np.random.rand())
    return probs

def predict_all_bikes(limit=20):
    results = []
    for bike_id in range(1, limit + 1):
        results.append({
            "bike_id": bike_id,
            "probabilities": predict_bike(bike_id)
        })
    return results
