### cleaning the data

import pandas as pd
import numpy as np

def load_clean_csv(filepath):
    try:
        raw = pd.read_csv(filepath, header=None,on_bad_lines='skip')
    except TypeError:
        # older pandas versions
        raw = pd.read_csv(filepath, header=None, error_bad_lines=False)
    for col_name, col_data in raw.items():
        if pd.to_numeric(col_data, errors='coerce').notna().mean() < 0.5:
            continue

        last_string_idx = 0

        for i, value in enumerate(col_data):
            try:
                float(value)
                if pd.isna(value):
                    raise ValueError
                break
            except (ValueError, TypeError):
                if pd.notna(value):  # only update if value is not NaN
                    last_string_idx = i


        header = col_data.iloc[last_string_idx]
        data = pd.to_numeric(col_data.iloc[last_string_idx + 1:], errors='coerce')
        data = data.interpolate().reset_index(drop = True)
        data.name = header

        raw[col_name] = data
        raw.rename(columns={col_name: header}, inplace=True)

    raw.dropna(axis=1, how='all', inplace=True)
    raw = raw.loc[:, raw.dtypes == float]
    min_length = raw.count().min()
    return raw.iloc[:min_length]