import pandas as pd

REQUIRED_COLUMNS = ['Wavelength', 'Air Ref', '20%', '40%', '60%', '80%', '100%']

def validate_excel_format(df: pd.DataFrame) -> list:
    
    error = []

    # Check column length
    if len(df.columns) != len(REQUIRED_COLUMNS):
        error.append(f"Invalid number of columns. Expected {len(REQUIRED_COLUMNS)}, got {len(df.columns)}")
    
    # Check for NaN values
    if df.isnull().values.any():
        error.append("Data contains NaN values.")

    return error


    
