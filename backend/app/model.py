import pandas as pd
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.stats import linregress

SMOOTH_FRAC = 0.00622

def preprocessing(file):
    # Read the CSV file
    df = pd.read_csv(file)
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

def algorithms_trend_detection(wavelength, transmittance):
    trans_arr = transmittance.values
    result = []


