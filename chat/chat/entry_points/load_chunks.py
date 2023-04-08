from collections import defaultdict
from collections.abc import Mapping
import logging

from PyPDF2.errors import DependencyError
from ..chunk import extract_keywords, split_to_chunk
from ..db import db_con, query
from ..pdf import extract


LOGGER = logging.getLogger(__name__)


def count_words(ss: list[str]) -> Mapping[str, int]:
    ret: defaultdict[str, int] = defaultdict(int)
    for s in ss:
        ret[s] += 1
    return ret


def load_chunks():
    df = query("""
    select
      id,
      content
    from
      pdfs
""")
    LOGGER.info("load data: number of rows = %d", len(df))
    con = db_con()
    for i in range(len(df)):
        LOGGER.info("processing %d-th file.", i)
        pdf_id = int(df["id"].iloc[i])
        try:
            bs = df["content"].iloc[i]
            try:
                text = extract(bs)
            except DependencyError:
                LOGGER.warn("pdf_id %d is invalid. skip.", pdf_id)
                continue
            chunks = split_to_chunk(text, 300)
            for j, chunk in enumerate(chunks):
                LOGGER.info("processing %d-th chunk.", j)
                keywords = extract_keywords(chunk)
                con.execute("""
                insert into chunks (
                  pdf_id,
                  position,
                  content

                ) values (
                  ?,
                  ?,
                  ?
                )
                """, [pdf_id, j, chunk])
                cur = con.execute("select last_insert_rowid() as chunk_id;")
                row = cur.fetchone()
                chunk_id: int = row["chunk_id"]
                counts = count_words(keywords)
                for k, v in counts.items():
                    con.execute("""
                    insert into keywords (
                      chunk_id,
                      word,
                      count
                    ) values (
                      ?,
                      ?,
                      ?
                    )
                    """, [chunk_id, k, v])
                con.commit()
        except Exception as ex:
            LOGGER.error("unknown error: pdf_id %d, %s", pdf_id, ex)
            LOGGER.warn("parsing pdf_id %d results in error. skip.", pdf_id)
            continue
