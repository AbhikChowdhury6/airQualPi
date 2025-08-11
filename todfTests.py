import pandas as pd
import csv
from icecream import ic
file_name = "abhik_bathroompi_Bosch_bme280_pressure-pa_internal_2025-08-02T15+0000.csv"

def to_nullable_dtype(tok: str) -> str:
    if not tok: return tok
    t = tok.lower()
    if t.startswith("int"):   return "I" + t[1:]      # int32 -> Int32
    if t.startswith("float"): return "F" + t[1:]     # float64 -> Float64
    if t in ("bool","boolean"): return "boolean"
    if t == "string": return "string"                # pandas StringDtype
    return tok

with open(file_name, newline="") as f:
    reader = csv.reader(f)
    headers = next(reader)

# we're going to parse out the pandas data types
pandas_dtypes = [s.split('!')[2] for s in headers]
datetime_cols = [col for col, dtype in zip(headers, pandas_dtypes) if dtype == "datetime64[ns]"]
dtype_map = {col: to_nullable_dtype(dtype) for col, dtype in zip(headers, pandas_dtypes) if dtype != "datetime64[ns]"}
ic(datetime_cols, dtype_map, pandas_dtypes, headers)

# read it in as a dataframe with the types
df = pd.read_csv(
    file_name,
    skiprows=5,               # Skip the original header
    names=headers,
    dtype=dtype_map,
    parse_dates=datetime_cols
)