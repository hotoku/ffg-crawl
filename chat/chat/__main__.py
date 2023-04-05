import sqlite3
import click
import sys

from .db import db_con


@click.group()
def main():
    pass


@main.command()
def create_table():
    sql = """
create table chunks (
    id integer primary key autoincrement,
    file_id integer not null,
    position integer not null,
    keywords text not null
)
"""
    con = db_con()
    try:
        con.execute(sql)
        con.commit()
    except sqlite3.OperationalError as ex:
        if str(ex) == "table chunks already exists":
            sys.stderr.write("exists\n")
        else:
            raise ex


if __name__ == "__main__":
    main()
