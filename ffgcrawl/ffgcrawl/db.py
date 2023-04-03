import os
import sqlite3

class Db:
    @staticmethod
    def path() -> str:
        return "./db.sqlite"

    @classmethod
    def connect(cls) -> sqlite3.Connection:
        con = sqlite3.connect(cls.path())
        return con

def init_db():    
    path = Db.path()
    if os.path.exists(path):
        return
    sql = """
create table pdfs (
    url text not null,
    content blob not null,
    created_at text not null
);
create table texts (
    url text not null,
    content text not null,
    created_at text not null
);    
"""
    con = Db.connect()
    con.executescript(sql)
    con.commit()

if __name__ == "__main__":
    init_db()
