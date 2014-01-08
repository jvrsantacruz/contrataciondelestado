# -*- coding: utf-8 -*-
"""Contratacion

Usage:
    contratacion fetch [options ...] [--page=<N>] [--store=<FILE>] [--workers=<N>] [--async] [--max-retries=<N>]
    contratacion parse [options ...] [--store=<FILE>] [--db=<FILE>]

Commands:
    fetch       Download documents from the web page
    parse       Parse and store downloaded documents

Options:
    -h --help         See this help
    --version         Show version
    --page N          Skip previous pages when downloading [default: 1]
    --workers N       Max number of concurrent requests [default: 5]
    --store FILE      Database file for download store [default: store.sqlite]
    --db FILE         Database file for processed data [default: db.sqlite]
    --async           Do not way for a page to complete until getting the next one
    --max-retries N   Number of times to retry a failed request before dumping it [default: 3]
    -v --verbose      Increase output verbosity level (Use -vv for debug level)
"""
from docopt import docopt

from . import __version__


def fetch_documents(args):
    from . import fetcher
    from .helpers import to_int

    store = args.get('--store')
    async = args.get('--async')
    page = to_int(args.get('--page'))
    workers = to_int(args.get('--workers'))
    max_retries = to_int(args.get('--max-retries'))
    fetcher.fetch_documents(store_path=store, page=page, workers=workers,
                            async=async, max_retries=max_retries)


def parse_documents(args):
    from . import parser

    db = args.get('--db')
    store = args.get('--store')
    parser.parse_documents(store_path=store, database_path=db)


def configure_logging(args):
    from . import log

    verbosity = log.get_verbosity_level(args.get('--verbose'))
    log.configure(level=verbosity)


def main():
    args = docopt(__doc__, version=__version__)

    configure_logging(args)

    if args['fetch']:
        fetch_documents(args)
    elif args['parse']:
        parse_documents(args)
