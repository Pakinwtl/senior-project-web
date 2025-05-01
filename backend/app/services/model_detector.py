import numpy as np
import joblib
import pandas as pd
from app.utils.constants import WINDOW_SIZE, CONCENTRATIONS
from app.utils.preprocess import preprocessing, is_duplicate
from app.services.base import TrendDetector
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.stats import linregress




class ModelTrendDetector(TrendDetector): 
    def __init__(self, model_path: str = "app/models/svm_model.joblib", scaler_path: str = "app/models/scaler.joblib"):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path) if scaler_path else None

    def detect(self, file) -> list:
        transmttance, wavelength = preprocessing(file)
        trans_arr = transmttance.values

        data, meta, results = [], [], []
        for i in range(trans_arr.shape[0] - WINDOW_SIZE + 1):
            window = trans_arr[i:i + WINDOW_SIZE]
            min_vals = np.min(window, axis=0)[::-1]
            min_idx = np.argmin(window, axis=0)
            min_wv_idx = np.array([i + idx for idx in min_idx])[::-1]
            min_wv = wavelength[min_wv_idx].to_numpy()
            feature = np.hstack([min_vals])
            data.append(feature)

            # Store corresponding (wavelength, transmittance) pair
            window_wv = min_wv.tolist()
            window_trans = min_vals.tolist()
            meta.append((i, window_wv, window_trans))

        if not data:
            return []

        X = np.array(data)
        if self.scaler:
            X = self.scaler.transform(X)
        
        y_pred = self.model.predict(X)
        for (i, window_wv, window_trans), pred in zip(meta, y_pred):
            _, _, r, _, _ = linregress(CONCENTRATIONS, window_wv)
            if pred != 1:
                continue
            if r < 0.8 or np.all(np.diff(window_trans) > 0):
                continue
            if is_duplicate(window_wv, window_trans, results):
                continue
            if len(set(window_wv)) != len(window_wv) or len(set(window_trans)) != len(window_trans):
                continue
        


            results.append({
            "sample_index": i,
            "predicted_label": int(pred),
            "wavelengths": window_wv,
            "transmittance": window_trans,
            "r_value": r,
            "concentrations": CONCENTRATIONS.tolist()
            })

        return results
