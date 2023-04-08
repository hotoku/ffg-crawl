import logging

import pandas as pd

from ..db import db_con, query


LOGGER = logging.getLogger(__name__)


def create_keywords():
    sql = """
    drop table if exists keywords;
    create table if not exists keywords (
      id integer primary key autoincrement,
      chunk_id integer not null,
      word text not null,
      count integer not null
    )    
"""
    con = db_con()
    con.executescript(sql)
    con.commit()


def condition(word: str, a0: str) -> bool:
    return (
        word != "*" and
        a0 == "名詞"
    )


def load_keywords():
    df = query("""
    select
      chunk_id,
      word,
      attr0
    from
      words
""")
    LOGGER.info("load df. number of records = %d", len(df))
    word = df["word"]
    attr0 = df["attr0"]
    LOGGER.info("calculating flags")
    flags = [
        condition(w, a)
        for w, a in zip(word, attr0)
    ]
    LOGGER.info("filtering and couting data")
    df2: pd.DataFrame = (
        df
        .loc[flags, :]
        .assign(count=1)
        .groupby(["chunk_id", "word"])
        .count()
        .reset_index()
    )[["chunk_id", "word", "count"]]
    create_keywords()
    con = db_con()
    df2.to_sql("keywords", con, index=False, if_exists="append")
    con.commit()
