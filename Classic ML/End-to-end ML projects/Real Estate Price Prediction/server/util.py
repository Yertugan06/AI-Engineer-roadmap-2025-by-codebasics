import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path

# --- Globals ---
__locations = None
__model = None
__data_columns = None

# --- Constants ---
ARTIFACTS_PATH = Path(
    "./Classic ML/End-to-end ML projects/Real Estate Price Prediction/server/artifacts"
)


def get_location_names():
    return __locations


def load_saved_artifacts():
    global __locations, __model, __data_columns

    print("Loading saved artifacts")

    with open(ARTIFACTS_PATH / "columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    with open(ARTIFACTS_PATH / "model.pkl", "rb") as f:
        __model = pickle.load(f)

    print("Artifacts saved succesfully")


def get_estimated_price(total_sqft: float, bath: int, bhk: int, location: str):
    if __model is None or __data_columns is None:
        raise RuntimeError("Artifacts not loaded. Call load_saved_artifacts() first.")

    X = np.zeros((1, len(__data_columns)))
    try:
        location_index = __data_columns.index(location.lower())
    except:
        location_index = -1

    X[0, 0] = total_sqft
    X[0, 1] = bath
    X[0, 2] = bhk

    if location_index >= 0:
        X[0, location_index] = 1

    X_df = pd.DataFrame(X, columns=__data_columns)
    prediction = float(round(__model.predict(X_df)[0], 2))

    return prediction


if __name__ == "__main__":
    load_saved_artifacts()

    print(get_estimated_price(1000, 3, 3, "1st Phase JP Nagar"))
    print(get_estimated_price(1000, 2, 2, "1st Phase JP Nagar"))
    print(get_location_names())
