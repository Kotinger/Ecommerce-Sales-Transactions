from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT/"data"/"processed"

DB_USER = os.getenv("MYSQL_USER", "root")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DATABASE", "ecommerce_sales")


def read_password()-> str:
    env = os.environ.get("MYSQL_PASSWORD")
    if env:
        return env.strip()
    pass_file = ROOT/"pass.txt"
    if pass_file.exists():
        for line in pass_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                return line
    raise SystemExit("Нет пароля: MYSQL_PASSWORD или pass.txt")

def main()-> None:
    clean = pd.read_parquet(OUT_DIR/"clean.parquet")
    url = f"mysql+pymysql://{DB_USER}:{read_password()}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(url)
    clean.to_sql("clean_orders", engine, if_exists="replace", index=False, chunksize=5000)
    print("clean_orders:", len(clean), "rows")

if __name__ == "__main__":
    main()
