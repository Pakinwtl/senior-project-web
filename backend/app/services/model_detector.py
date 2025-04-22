from app.utils.constants import WINDOW_SIZE, CONCENTRATIONS
from app.utils.preprocess import preprocessing, is_duplicate
from app.services.base import TrendDetector
import numpy as np
import joblib

class ModelTrendDetector(TrendDetector): 
    def __init__(self, model_path: str = None, scaler_path: str = None):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path) if scaler_path else None

    def detect(self, file) -> list:
        transmttance, wavelength = preprocessing(file)
        trans_arr = transmttance.values

        data = []
        meta = []
        for i in range(trans_arr.shape[0] - WINDOW_SIZE + 1):
            window = trans_arr[i:i + WINDOW_SIZE]
            min_vals = np.min(window, axis=0)[::-1]
            min_idx = np.argmin(window, axis=0)[::-1]
            min_wv_idx = np.array([i + idx for idx in min_idx])
            min_wv = wavelength[min_wv_idx].to_numpy()
            feature = np.hstack([min_wv, min_vals])
            data.append(feature)

            # Store corresponding (wavelength, transmittance) pair
            window_wv = min_wv.tolist()
            window_trans = [window[idx, col] for col, idx in enumerate(min_idx)]
            meta.append((i, window_wv, window_trans))

        if not data:
           return []

        X = np.array(data)
        if self.scaler:
            X = self.scaler.transform(X)
        
        y_pred = self.model.predict(X)
        results = []
        for (i, window_wv, window_trans), pred in zip(meta, y_pred):
            if y_pred != 1:
                continue
            if is_duplicate(window_wv, window_trans, results):
                continue

        results.append({
        "sample_index": i,
        "predicted_label": int(pred),
        "wavelengths": window_wv,
        "transmittance": window_trans
        })

        return results

