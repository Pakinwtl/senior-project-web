import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from statsmodels.nonparametric.smoothers_lowess import lowess
from app.utils.constants import SMOOTH_FRAC
from app.utils.validate_excel import validate_excel_format

def preprocessing(file):
    # Read the CSV file%
    df = pd.read_excel(file)

    # Validate the format of the DataFrame
    errors = validate_excel_format(df)
    if errors:
        return JSONResponse(status_code=400, content={"errors": errors})
   

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
