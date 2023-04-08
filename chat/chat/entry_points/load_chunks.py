from collections import defaultdict
from collections.abc import Mapping
import logging

from PyPDF2.errors import DependencyError

from chat import is_debug
from ..chunk import morphological_analysis, split_to_chunk
from ..db import db_con, query
from ..pdf import extract


LOGGER = logging.getLogger(__name__)


def count_words(ss: list[str]) -> Mapping[str, int]:
    ret: defaultdict[str, int] = defaultdict(int)
    for s in ss:
        ret[s] += 1
    return ret


def create_chunks():
    con = db_con()
    sql = """
drop table if exists chunks;
create table chunks (
    id integer primary key autoincrement,
    pdf_id integer not null,
    position integer not null,
    content text not null
);
"""
    con.executescript(sql)
    con.commit()


def load_chunks():
    create_chunks()
    df = query("""
    select
      id,
      content
    from
      pdfs
""")
    if is_debug():
        df = df.iloc[:30, :]
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
                con.commit()
        except Exception as ex:
            LOGGER.error("unknown error: pdf_id %d, %s", pdf_id, ex)
            LOGGER.warn("parsing pdf_id %d results in error. skip.", pdf_id)
            continue
