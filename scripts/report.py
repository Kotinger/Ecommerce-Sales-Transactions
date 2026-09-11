from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT/"data"/"processed"

ORDER_COL = "order_id"
ORDER_KEY = "order_key"
CLIENT_COL = "customer_id"
MONEY_COL = "total_amount"
DATE_COL = "order_date"
DIM_COL = "region"

def load_tables()-> pd.DataFrame:
    return pd.read_parquet(OUT_DIR/"clean.parquet")

def kpi_totals(clean: pd.DataFrame)-> None:
    gmv = clean[MONEY_COL].sum()
    orders = clean[ORDER_COL].nunique()
    aov = gmv / orders
    print("gmv", gmv, "orders", orders, "aov", aov)

def kpi_by_dim(clean: pd.DataFrame)-> pd.DataFrame:
    check_dim = clean.groupby(DIM_COL, as_index=False).agg(
        gmv=(MONEY_COL, "sum"),
        orders=(ORDER_COL, "nunique"))
    check_dim["aov"] = check_dim["gmv"] / check_dim["orders"]
    print(check_dim.sort_values("gmv", ascending=False))
    return check_dim

def kpi_year_month(clean: pd.DataFrame)-> pd.DataFrame:
    m = clean.copy()
    m["year"] = m[DATE_COL].dt.year
    m["month"] = m[DATE_COL].dt.month
    check_y_m = m.groupby(["year", "month"], as_index=False).agg(
        gmv=(MONEY_COL, "sum"),
        orders=(ORDER_COL, "nunique"))
    check_y_m["aov"] = check_y_m["gmv"] / check_y_m["orders"]
    print(check_y_m.sort_values(["year", "month"]))
    return check_y_m

def main()-> None:
    clean = load_tables()
    kpi_totals(clean)
    kpi_by_dim(clean)
    kpi_year_month(clean)

if __name__ == "__main__":
    main()
