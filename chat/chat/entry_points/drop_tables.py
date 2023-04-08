from collections.abc import Iterable
import logging

import click

from ..db import db_con

LOGGER = logging.getLogger(__name__)


def drop_query(table: str) -> str:
    return f"""
drop table if exists {table}
"""


_TARGET_TABLES = [
    "chunks",
    "keywords",
    "words",
    "tfidfs",
    "document_counts"
]


@click.argument("tables", nargs=-1)
def drop_tables(tables: Iterable[str]):
    for t in tables:
        if not t in _TARGET_TABLES:
            raise ValueError(f"{t} can not be deleted.")

    con = db_con()
    for t in tables:
        LOGGER.info("droping %s", t)
        con.execute(drop_query(t))

    con.commit()
