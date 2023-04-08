import numpy as np

from ..db import db_con, query


def load_tcidfs2():
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
with min_id as (
    select
      chunk_id,
      min(id) as min_id
    from
      keywords
    group by
      chunk_id
),
keywords2 as (
    select
      k.chunk_id,
      k.count,
      k.word
    from
      keywords k
        left join
      min_id m
        on k.chunk_id = m.chunk_id
    where
      k.id <= m.min_id + 80 - 1
)
select
  k.chunk_id,
  k.word,
  1.0 * k.count as term_count,
  1.0 * dc.document_count / 
    (select count(distinct chunk_id) from keywords) as document_frequency
from
  keywords2 k
    inner join
  document_counts dc
    on k.word = dc.word
"""
    tcidf = (
        query(sql2)
        .assign(
            tcidf=lambda df: df["term_count"] *
            np.log(1/df["document_frequency"])
        )
    )
    con.execute("drop table if exists tcidfs2")
    tcidf.to_sql("tcidfs2", con, index=False)
    con.commit()
