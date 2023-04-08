import logging
import sqlite3
import sys

from ..db import db_con

LOGGER = logging.getLogger(__name__)


def drop_tables():
    con = db_con()
    sql = """
drop table if exists chunks
"""
    sql2 = """
drop table if exists keywords
"""
    LOGGER.info("droping chunks")
    con.execute(sql)
    LOGGER.info("droping keywords")
    con.execute(sql2)
    con.commit()
