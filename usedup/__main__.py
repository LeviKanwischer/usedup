# -*- coding: utf-8 -*-

"""
Datamine (Upsight.com) CLI Admin Tools

usedup is a simple command line tool for performing basic admin tasks
using both official and unofficial datamine api's. At present this allows
for; checking currently running queries, viewing a running queries stats,
killing active queries, and/or downloading an archive of historicly run
queries. Since login is required to access datamine(upsight.com), user
credentials will be asked upon submitting each command.

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

    usedup is a simple command line tool for performing basic admin tasks
    using both official and unofficial datamine api's. At present this allows
    for; checking currently running queries, viewing a running queries stats,
    killing active queries, and/or downloading an archive of historicly run
    queries. Since login is required to access datamine(upsight.com), user
    credentials will be asked upon submitting each command.

        USAGE:
        $ usedup --help

    See the README for further details.
    """
    pass


@cli.command()
@click.option('--period', '-p', help='Observation Period')
@click.option('--outfile', '-o', help='Output file (.csv)')
def history(period='1wk', outfile=None):
    """Download an archive of previously run queries.

    Period Options:

    1wk=='1 week'; 2wk=='2 weeks'; 1mt=='1 month'; 2mt=='2 months'; 3mt=='3 months'

    Output File: Saves to downloads if missing.
    """
    UsedUp().history(period=period, outfile=outfile)


@cli.command()
@click.option('--continuous', '-c', is_flag=True, help='Runs indefinately.')
@click.option('--pause', '-p', default=60, help='Seconds between checks.')
def running(continuous, pause):
    """Print list of currently running queries."""
    usedup = UsedUp()
    usedup.running()
    while continuous:
        time.sleep(pause)
        usedup.running()


@cli.command()
@click.argument('query_ids', nargs=-1)
def kill(query_ids):
    """Kill actively running query using Upsight's Query ID."""
    usedup = UsedUp()
    for query_id in query_ids:
        usedup.kill(query_id=query_id)


@cli.command()
@click.argument('query_ids', nargs=-1)
@click.option('--detail/--no-detail', default=True, help='Show detail (Y/n)')
@click.option('--query/--no-query', default=True, help='Show SQL (Y/n)')
def details(query_ids, detail, query):
    """Print details about active query Upsight's Query ID."""
    usedup = UsedUp()
    for query_id in query_ids:
        usedup.details(query_id, detail, query)
