import pandas as pd
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.stats import linregress

svm_model = None
scaler = None

SMOOTH_FRAC = 0.00622
WINDOW_SIZE = 30
CONCENTRATIONS = np.array([20, 40, 60, 80, 100])

def preprocessing(file):
    # Read the CSV file%
    df = pd.read_excel(file)
    df = df[(df.iloc[:, 0] > 450 ) & (df.iloc[:, 0] < 950)]
    wavelength = df.iloc[:, 0].reset_index(drop=True)
    air_ref = df.iloc[:, 1].reset_index(drop=True)
    intensity = df.iloc[:, 2:].reset_index(drop=True)
    
    trans = intensity.div(air_ref, axis=0)

    smoothed = pd.DataFrame()
    for col in trans.columns:
        smooth = lowess(trans[col], wavelength, frac=SMOOTH_FRAC)
        smoothed[col] = smooth[:, 1]
    
    return smoothed, wavelength


def is_duplicate(new_wv, new_trans, existing_results, tol=1e-5):
    for result in existing_results:
        if (np.allclose(result["wavelengths"], new_wv, atol=tol) and
            np.allclose(result["transmittance"], new_trans, atol=tol)):
            return True
    return False


def algorithms_trend_detection(wavelength, transmittance):
    trans_arr = transmittance.values
    results = []
    for i in range(trans_arr.shape[0] - WINDOW_SIZE + 1):
        window = trans_arr[i:i + WINDOW_SIZE]
        min_vals = np.min(window, axis=0)
        min_idx = np.argmin(window, axis=0)

        if np.any(min_idx == 0) or np.any(min_idx == WINDOW_SIZE - 1):
            continue

        min_vals = min_vals[::-1]
        min_wv_idx = np.array([i + idx for idx in min_idx])[::-1]
        min_wv = wavelength[min_wv_idx].to_numpy()
        _, _, r, _, _ = linregress(CONCENTRATIONS, min_wv)

        label = 1 if abs(r) >= 0.8 and np.all(np.diff(min_vals) < 0) else 0
        if label == 0:
            continue

        # Store wavelength and corresponding transmittance values (one-to-one)
        window_wv = min_wv.tolist()
        window_trans = [window[idx, col] for col, idx in enumerate(min_idx[::-1])]

        if is_duplicate(window_wv, window_trans, results):
            continue

        results.append({
            "sample_index": i,
            "predicted_label": label,
            "wavelengths": window_wv,
            "transmittance": window_trans
        })

    return results


def model_trend_detection(file, use_model=True):
    smoothed_trans, wavelength = preprocessing(file)
    trans_arr = smoothed_trans.values

    if not use_model:
        return algorithms_trend_detection(wavelength, smoothed_trans)

    # ========== MODEL-BASED PREDICTION ==========
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
    X_scaled = scaler.transform(X)
    y_pred = svm_model.predict(X_scaled)

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



