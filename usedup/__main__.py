# -*- coding: utf-8 -*-

"""
Datamine (Upsight.com) CLI Admin Tools

usedup is a simple command line tool for performing basic admin tasks.
At present this allows for; checking currently running queries, viewing
a running queries stats, killing active queries, and/or extracting user
run query archives. Since login is required to access Upsight.com, user
credentials are stored in plain test in a ~/.usedup.ini file.

    USAGE:
    $ usedup --help

See the README for further details.
"""

import time

import click

from usedup import UsedUp


@click.group()
def cli():
    """
    Datamine (Upsight.com) CLI Admin Tools

    usedup is a simple command line tool for performing basic admin tasks.
    At present this allows for; checking currently running queries, viewing
    a running queries stats, killing active queries, and/or extracting user
    run query archives. Since login is required to access Upsight.com, user
    credentials are stored in plain test in a ~/.usedup.ini file.

        USAGE:
        $ usedup --help

    See the README for further details.
    """
    pass


@cli.command()
@click.argument('period')
def history(period='1wk'):
    """Extract past user queries.

    `period` == 1wk, 2wk, 1mt, 2mt, 3mt
    """
    UsedUp().history(period=period)


@cli.command()
@click.option('--continuous', '-c', is_flag=True, help='Run indefinately.')
@click.option('--pause', '-p', default=60, help='Seconds between checks.')
def running(continuous, pause):
    """Currently running queries."""
    usedup = UsedUp()
    usedup.running()
    while continuous:
        time.sleep(pause)
        usedup.running()


@cli.command()
@click.argument('ids', nargs=-1)
def kill(ids):
    """Cancel active query.

    `ids` == Upsight's Query ID
    """
    usedup = UsedUp()
    for qid in ids:
        usedup.kill(qid=qid)


@cli.command()
@click.argument('ids', nargs=-1)
@click.option('--detail/--no-detail', default=True, help='Show details?')
@click.option('--query/--no-query', default=True, help='Show query?')
def details(ids, detail, query):
    """View active query details.

    `ids` == Upsight's Query ID
    """
    usedup = UsedUp()
    for qid in ids:
        usedup.details(qid, detail, query)
