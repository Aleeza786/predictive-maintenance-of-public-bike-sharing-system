import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.dummy import DummyClassifier
import joblib
import os

components = ["brakes", "chain", "tires"]

# Correct path to project root (3 levels up from current file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
data_dir = os.path.join(BASE_DIR, "data-gen")
model_dir = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(model_dir, exist_ok=True)

def train_component(X, y, comp):
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    except Exception as e:
        print(f"[{comp}] small dataset, fallback to dummy model ({e})")
        model = DummyClassifier(strategy="uniform")
        model.fit(X, y)
        joblib.dump(model, os.path.join(model_dir, f"{comp}_model.joblib"))
        return

    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)
    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    print(f"[{comp}] AUC={auc:.2f}")
    joblib.dump(model, os.path.join(model_dir, f"{comp}_model.joblib"))

def main():
    df_path = os.path.join(data_dir, "train.csv")
    if not os.path.exists(df_path):
        raise FileNotFoundError(f"Missing file: {df_path}\nPlease run generate_data.py first.")

    df = pd.read_csv(df_path)
    features = df.drop(columns=["bike_id", "component_failed"], errors='ignore')

    for comp in components:
        y = df.get(f"target_{comp}")
        if y is None:
            print(f"[WARN] Column target_{comp} not found, skipping.")
            continue
        train_component(features, y, comp)

if __name__ == "__main__":
    main()
