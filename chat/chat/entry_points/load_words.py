from ..chunk import morphological_analysis
from ..db import db_con, query


def create_words():
    con = db_con()
    sql = """
drop table if exists words;
create table words (
    id integer primary key autoincrement,
    chunk_id integer not null,
    word text not null,
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
    con = db_con()
    for i in range(len(df)):
        chunk_id = df["id"].iloc[i]
        text = df["content"].iloc[i]
        infos = morphological_analysis(text)
        for info in infos:
            con.execute("""
            insert into
            words (
              chunk_id,
              word,
              attributes
            )
            values (
              ?,
              ?,
              ?
            )
            """, [chunk_id,
                  info.word,
                  repr(info.attributes)])
        con.commit()
