import logging
import sqlite3
import sys

from ..db import db_con

LOGGER = logging.getLogger(__name__)


def create_tables():
    con = db_con()
    sql = """
create table if not exists chunks (
    id integer primary key autoincrement,
    pdf_id integer not null,
    position integer not null,
    content text not null
)
"""
    sql2 = """
create table if not exists keywords (
    id integer primary key autoincrement,
    chunk_id integer not null,
    word text not null,
    count integer not null
)    
"""
    LOGGER.info("creating chunks")
    con.execute(sql)
    LOGGER.info("creating keywords")
    con.execute(sql2)
    con.commit()
