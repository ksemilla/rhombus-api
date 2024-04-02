from celery import shared_task
import pandas as pd
import numpy as np
import time
from ingests.models import Ingest, Column, Record
import math
import time
import re

def string_to_attribute_name(s):
    # Replace invalid characters with underscores
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    # Ensure the name starts with a letter or an underscore
    if not s[0].isalpha() and s[0] != '_':
        s = '_' + s
    return s

@shared_task
def infer_and_convert_data_types(df, numeric_threshold=0.5, datetime_threshold=0.5, datetime_format=None):
    for col in df.columns:
        # Filter out empty values
        non_empty_data = df[col].dropna()

        # Attempt to convert to numeric
        df_numeric = pd.to_numeric(non_empty_data, errors='coerce')
        numeric_ratio = (~df_numeric.isna()).mean()
        
        # Attempt to convert to datetime
        df_datetime = pd.to_datetime(non_empty_data, errors='coerce', format=datetime_format)
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
        elif len(non_empty_data) == 0:
            df[col] = df[col].astype(object)
        elif len(non_empty_data.unique()) / len(non_empty_data) < 0.5:
            df[col] = non_empty_data.astype('category')

    return df

@shared_task
def process_file(ingest_id):
    start_time = time.time()
    ingest = Ingest.objects.get(id=ingest_id)
    try:
        with ingest.file.open() as f:
            if ingest.file_name.endswith(".xlsx"):
                df = pd.read_excel(f)
            elif ingest.file_name.endswith(".csv"):
                df = pd.read_csv(f)
            else:
                raise ValueError({ "message": "File should be csv or excel (.xlsx)" })
            df = infer_and_convert_data_types(df)

            ingest.row_nums = df.shape[0]
            ingest.save()

            df.rename(columns={col: string_to_attribute_name(col) for col in df.columns}, inplace=True)
            fields = []

            # Create Columns objects
            for index, (field, dtype) in enumerate(df.dtypes.items()):
                Column.objects.create(
                    ingest=ingest,
                    label=field,
                    value=field,
                    dtype=dtype,
                    display_order=index
                )
                fields.append((field, dtype,))

            # Create Record objects, rows
            for idx, row in enumerate(df.itertuples(index=False)):
                data = {}
                for field, dtype in fields:
                    value = getattr(row, field)
                    if dtype == "datetime64[ns]":
                        data[field] = value.isoformat() if value else ""
                    elif isinstance(value, float) and math.isnan(value):
                        data[field] = ""
                    else:
                        data[field] = value

                Record.objects.create(
                    ingest=ingest,
                    data=data
                )
                
                if idx % 20 == 0:
                    ingest.processed_row_nums = idx + 1
                    ingest.save()
                    time.sleep(0.1)
            ingest.processed_row_nums = ingest.row_nums    

        ingest.status = Ingest.Status.COMPLETED
    except Exception as e:
        print(e)
        ingest.status = Ingest.Status.FAILED
    
    end_time = time.time()
    ingest.process_time = end_time - start_time
    ingest.save()