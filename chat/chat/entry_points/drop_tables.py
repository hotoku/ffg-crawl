import logging
import sqlite3
import sys

from ..db import db_con

LOGGER = logging.getLogger(__name__)


def drop_query(table: str) -> str:
    return f"""
drop table if exists {table}
"""


def drop_tables():
    con = db_con()

    for table in ["chunks", "keywords", "words", "tfidfs", "document_counts"]:
        LOGGER.info("droping %s", table)
        con.execute(drop_query(table))

    con.commit()
