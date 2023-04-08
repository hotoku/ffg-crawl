import logging
import click
import sys


from .entry_points import (
    load_chunks as load_chunks_impl,
    drop_tables as drop_tables_impl,
    load_tfidfs as load_tfidfs_impl,
    load_tcidfs as load_tcidfs_impl,
    load_tcidfs2 as load_tcidfs2_impl,
    load_words as load_words_impl,
    clear_cache as clear_cache_impl,
    load_keywords as load_keywords_impl,
    ask as ask_impl
)

from . import set_debug_flag


LOGGER = logging.getLogger(__name__)


def setup_logging(debug: bool):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s",
        stream=sys.stderr
    )


@click.group()
@click.option("--debug/--nodebug", is_flag=True, default=False)
def main(debug: bool):
    setup_logging(debug)
    set_debug_flag(debug)


load_chunks = main.command(load_chunks_impl)
load_words = main.command(load_words_impl)
load_keywords = main.command(load_keywords_impl)
load_tfidfs = main.command(load_tfidfs_impl)
load_tcidfs = main.command(load_tcidfs_impl)
load_tcidfs2 = main.command(load_tcidfs2_impl)

drop_tables = main.command(drop_tables_impl)
clear_cache = main.command(clear_cache_impl)

ask = main.command(ask_impl)

if __name__ == "__main__":
    main()
