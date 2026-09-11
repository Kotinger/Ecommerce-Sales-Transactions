from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT/"data"
OUT_DIR = DATA_DIR/"processed"
RAW_PATH = DATA_DIR/"ecommerce_sales_34500.csv"

ORDER_COL = "order_id"
ORDER_KEY = "order_key"
CLIENT_COL = "customer_id"
MONEY_COL = "total_amount"
DATE_COL = "order_date"

NEED_PEOPLE = False

def load_data(path: Path)-> pd.DataFrame:
    df = pd.read_csv(path)
    print(df.shape)
    print(df.columns.to_list())
    print(df.isna().sum())
    print(df.dtypes)
    return df

def chek_gain(df: pd.DataFrame)-> str:
    rows, orders = len(df), df[ORDER_COL].nunique()
    grain = "line" if rows > orders else "order"
    print("rows", rows, "orders", orders, "->", grain)
    return grain

#order_date str
def prepare_types(df: pd.DataFrame)-> pd.DataFrame:
    df = df.copy()
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], dayfirst=False, errors="coerce")
    print("date", df[DATE_COL].min(), "->", df[DATE_COL].max())
    return df

def build_clean(df: pd.DataFrame)-> pd.DataFrame:
    clean = df.copy()
    print(len(clean))
    if MONEY_COL in clean.columns:
        clean = clean[clean[MONEY_COL] > 0]
        print("money > 0", len(clean))
    print("orders", clean[ORDER_COL].nunique())
    return clean

def sanity_check(raw: pd.DataFrame, clean: pd.DataFrame)-> None:
    print("---sanity----")
    print("rows", len(raw), "->", len(clean))
    print("orders", raw[ORDER_COL].nunique(), "->", clean[ORDER_COL].nunique())
    print("dates", clean[DATE_COL].min(), "->", clean[DATE_COL].max())

# в описании сказано что уникальные, но на всякий случий проверим
def add_keys(clean: pd.DataFrame)-> pd.DataFrame:
    clean = clean.copy()
    check = clean.groupby(ORDER_COL)[CLIENT_COL].nunique()
    bad = (check > 1)
    print(bad.sum())
    clean[ORDER_KEY] = clean[ORDER_COL].astype(str)
    return clean

def save_tables(clean: pd.DataFrame)-> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    clean.to_parquet(OUT_DIR/"clean.parquet", index=False)
    print("saved", OUT_DIR)

def main()-> None:
    raw = load_data(RAW_PATH)
    chek_gain(raw)
    df = prepare_types(raw)
    clean = build_clean(df)
    sanity_check(raw, clean)
    clean = add_keys(clean)
    save_tables(clean)

if __name__ == "__main__":
    main()
