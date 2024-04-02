import pandas as pd
import numpy as np

def infer_and_convert_data_types(df, numeric_threshold=0.5, datetime_threshold=0.5):
    for col in df.columns:
        # Filter out empty values
        non_empty_data = df[col].dropna()

        # Attempt to convert to numeric
        df_numeric = pd.to_numeric(non_empty_data, errors='coerce')
        numeric_ratio = (~df_numeric.isna()).mean()
        
        # Attempt to convert to datetime
        df_datetime = pd.to_datetime(non_empty_data, errors='coerce')
        non_null_datetime_ratio = (~df_datetime.isna()).mean()
        
        # Determine data type based on thresholds
        if numeric_ratio >= numeric_threshold:
            if np.issubdtype(df_numeric.dtype, np.integer):
                df[col] = df_numeric.astype(int)
            elif np.issubdtype(df_numeric.dtype, np.floating):
                df[col] = df_numeric.astype(float)
            elif np.issubdtype(df_numeric.dtype, np.complexfloating):
                df[col] = df_numeric.astype(complex)
            elif np.issubdtype(df_numeric.dtype, np.bool_):
                df[col] = df_numeric.astype(bool)
        elif non_null_datetime_ratio >= datetime_threshold:
            df[col] = df_datetime
        elif len(non_empty_data.unique()) / len(non_empty_data) < 0.5:
            df[col] = non_empty_data.astype('category')

    return df