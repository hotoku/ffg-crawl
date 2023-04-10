import logging
from ..chunk import morphological_analysis
from ..db import db_con, query

LOGGER = logging.getLogger(__name__)


def create_words():
    con = db_con()
    sql = """
drop table if exists words;
create table words (
    id integer primary key autoincrement,
    chunk_id integer not null,
    word text not null,
    attr0 text not null,
    attr1 text not null,
    attributes text not null
);
"""
    con.executescript(sql)
    con.commit()


def load_words():
    create_words()
    df = query("""
    select
      id,
      content
    from
      chunks
""")
    LOGGER.info("load df. number of records = %d", len(df))
    con = db_con()
    for i in range(len(df)):
        LOGGER.info("start %d-th chunk", i)
        chunk_id = int(df["id"].iloc[i])
        text = df["content"].iloc[i]
        infos = morphological_analysis(text)
        for info in infos:
            con.execute("""
            insert into
            words (
              chunk_id,
              word,
              attr0,
              attr1,
              attributes
            )
            values (
              ?,
              ?,
              ?,
              ?,
              ?
            )
            """, [chunk_id,
                  info.word,
                  info.attributes[0],
                  info.attributes[1],
                  repr(info.attributes)])
        con.commit()
