def load_clean_csv(filepath):
    import io
    import pandas as pd

    if hasattr(filepath, 'read'):
        content = filepath.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8')
    else:
        with open(filepath, 'r') as f:
            content = f.read()

    lines = content.split('\n')
    max_cols = max(len(line.split(',')) for line in lines if line.strip())
    raw = pd.read_csv(io.StringIO(content), header=None, names=range(max_cols))

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
                if pd.notna(value):
                    last_string_idx = i
        header = col_data.iloc[last_string_idx]
        data = pd.to_numeric(col_data.iloc[last_string_idx + 1:], errors='coerce')
        data = data.interpolate().reset_index(drop=True)
        data.name = header
        raw[col_name] = data
        raw.rename(columns={col_name: header}, inplace=True)

    raw.dropna(axis=1, how='all', inplace=True)
    raw = raw.loc[:, raw.dtypes == float]

    min_length = int(raw.count().min())
    return raw.iloc[:min_length]