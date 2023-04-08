import numpy as np

from ..db import db_con, query


def load_tfidfs():
    con = db_con()
    sql1 = """
drop table if exists document_counts;
create table document_counts as
select
  word,
  count(distinct chunk_id) as document_count
from
  keywords
group by
  word;    
"""
    con.executescript(sql1)

    sql2 = """
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
  document_counts dc
    on tf.word = dc.word
"""
    tfidf = (
        query(sql2)
        .assign(
            tfidf=lambda df: df["term_frequency"] *
            np.log(1/df["document_frequency"])
        )
    )
    con.execute("drop table if exists tfidfs")
    tfidf.to_sql("tfidfs", con, index=False)
    con.commit()
