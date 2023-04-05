import sqlite3
import pandas as pd

_DB_PATH = "../ffgcrawl/db.sqlite"


def db_con() -> sqlite3.Connection:
    con: sqlite3.Connection = sqlite3.connect(_DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def query(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, db_con())
