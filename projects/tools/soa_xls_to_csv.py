"""Convert an SOA mort.soa.org .xls table export to a clean two-column CSV.

Usage: python soa_xls_to_csv.py <input.xls> <output.csv> <value_column_name>

The SOA export has a metadata block, then a 'Row\\Column' header row, then
one row per age with the rate stored as text. This writes `age,<value>`.
"""
import sys

import pandas as pd
import xlrd


def read_soa_table(path):
    sheet = xlrd.open_workbook(path).sheet_by_index(0)
    meta, start = {}, None
    for r in range(sheet.nrows):
        key, *rest = sheet.row_values(r)
        key = str(key).strip()
        if key.startswith("Row\\Column"):
            start = r + 1
            break
        if key.endswith(":") and rest:
            meta.setdefault(key.rstrip(":"), str(rest[0]).strip())
    if start is None:
        raise ValueError(f"{path}: no 'Row\\Column' header found")
    rows = [sheet.row_values(r)[:2] for r in range(start, sheet.nrows)]
    df = pd.DataFrame(rows, columns=["age", "value"])
    df = df[df["age"].astype(str).str.strip() != ""]
    df["age"] = df["age"].astype(float).astype(int)
    df["value"] = df["value"].astype(float)
    return meta, df


def main():
    src, dst, col = sys.argv[1:4]
    meta, df = read_soa_table(src)
    lo, hi = int(meta["Row, Column (if applicable)->MinScaleValue"]), int(
        meta["Row, Column (if applicable)->MaxScaleValue"])
    assert list(df["age"]) == list(range(lo, hi + 1)), "ages not contiguous"
    assert df["value"].between(0, 1).all(), "rate outside [0, 1]"
    df.rename(columns={"value": col}).to_csv(dst, index=False)
    print(f"{src} -> {dst}: {meta['Table Name']} | ages {lo}-{hi} | {len(df)} rows")


if __name__ == "__main__":
    main()
