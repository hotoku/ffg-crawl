import numpy as np

from ..db import db_con, query


def load_tfidf():
    sql = """
with document_length as (
    select
      chunk_id,
      sum(count) as length
    from
      keywords
    group by
      chunk_id
), term_frequency as (
    select
      k.chunk_id,
      k.word,
      k.count,
      dl.length
    from
      keywords k
        inner join
      document_length dl
        on k.chunk_id = dl.chunk_id
), document_count as (
    select
      word,
      count(distinct chunk_id) as document_count
    from
      keywords
    group by
      word      
)
select
  tf.chunk_id,
  tf.word,
  1.0 * tf.count /
    tf.length as term_frequency,
  1.0 * dc.document_count / 
    (select count(distinct chunk_id) from keywords) as document_frequency
from
  term_frequency tf
    inner join
  document_count dc
    on tf.word = dc.word
"""
    tfidf = (
        query(sql)
        .assign(
            tfidf=lambda df: df["term_frequency"] *
            np.log(1/df["document_count"])
        )
    )
    con = db_con()
    con.execute("drop table if exists tfidf")
    tfidf.to_sql("tfidf", con)
    con.commit()
