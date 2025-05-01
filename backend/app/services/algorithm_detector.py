from app.services.base import TrendDetector
from app.utils.preprocess import preprocessing, is_duplicate
from app.utils.constants import WINDOW_SIZE, CONCENTRATIONS
from scipy.stats import linregress
import numpy as np


class AlgorithmsTrendDetector(TrendDetector):
    def detect(self, file) -> list :
        transmittance, wavelength = preprocessing(file)
        trans_arr = transmittance.values
        results = []

        for i in range(trans_arr.shape[0] - WINDOW_SIZE + 1):
            window = trans_arr[i:i + WINDOW_SIZE]
            min_vals = np.min(window, axis=0)
            min_idx = np.argmin(window, axis=0)
            min_wv = wavelength[i + min_idx].to_numpy()

            min_vals = min_vals[::-1]
            min_wv = min_wv[::-1]

            if np.any(min_idx == 0) or np.any(min_idx == WINDOW_SIZE - 1) or not np.all(np.diff(min_vals) < 0):
                continue

            _, _, r, _, _ = linregress(CONCENTRATIONS, min_wv)

            label = 1 if abs(r) >= 0.8 else 0  

            if label == 0:
                continue

            window_wv = min_wv.tolist()
            window_trans = min_vals.tolist()

            if is_duplicate(window_wv, window_trans, results):
                continue

            results.append({
                "sample_index": i,
                "predicted_label": label,
                "wavelengths": window_wv,
                "transmittance": window_trans,
                "r_value": abs(r),
                "concentrations": CONCENTRATIONS.tolist()
            })

        return results
        


