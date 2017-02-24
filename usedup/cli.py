# -*- coding: utf-8 -*-

"""DataMine (Upsight.com) CLI Admin Tool

usedup is a simple command line tool for performing basic admin tasks
using both official and unofficial DataMine api's. At present this allows
for; checking currently running queries, viewing a running queries stats,
killing active queries, and/or downloading an archive of historically run
queries. Since login is required to access DataMine(Upsight.com), user
credentials will be asked upon submitting each command.

USAGE:
    $ usedup --help

See the README for further details.

"""
from __future__ import print_function

import time

import click
from tabulate import tabulate

from usedup.core import UsedUp


@click.group()
def main():
    """
    DataMine (Upsight.com) CLI Admin Tool

    usedup is a simple command line tool for performing basic admin tasks
    using both official and unofficial DataMine api's. At present this allows
    for; checking currently running queries, viewing a running queries stats,
    killing active queries, and/or downloading an archive of historically run
    queries. Since login is required to access DataMine(Upsight.com), user
    credentials will be asked upon submitting each command.

    USAGE:
        $ usedup --help

    See the README for further details.

    """
    pass


@main.command()
@click.option('--period', '-p', default='1wk', help='DataMine periods back from now.')
@click.option('--outfile', '-o', help='Output file save location (.csv)')
def history(period, outfile):
    """Download an archive of previously run queries.

    Period Options:
    1wk=='1 week';
    2wk=='2 weeks';
    1mt=='1 month';
    2mt=='2 months';
    3mt=='3 months';

    Output File: Saves to current path if missing.

    """
    with UsedUp() as usedup:
        usedup.history(period=period, outfile=outfile)


@main.command()
@click.argument('qids', nargs=-1)
def kill(qids):
    """Kill actively running query using Upsight's Query ID."""
    with UsedUp() as usedup:
        for qid in qids:
            result = usedup.kill(qid=qid)
            print('QueryID %s canceled successfully? %s' % (qid, result))


@main.command()
@click.option('--continuous', '-c', is_flag=True, help='Run indefinately.')
@click.option('--pause', '-p', default=60, help='Seconds between checks.')
def running(continuous, pause):
    """Print list of currently running queries."""
    showresults = True
    with UsedUp() as usedup:
        while showresults:
            queries = usedup.running()
            tabbed = tabulate(queries, headers='keys', tablefmt="grid")
            print(tabbed)
            showresults = continuous
            time.sleep(pause)


@main.command()
@click.argument('qids', nargs=-1)
@click.option('--no-details', '-nd', is_flag=False, help='Exclude processing details.')
@click.option('--no-query', '-nq', is_flag=False, help='Exclude query string.')
def status(qids, details, query):
    """Print details about active query Upsight's Query ID."""
    with UsedUp() as usedup:
        for qid in qids:
            result = usedup.status(qid, details, query)

            if result is None:
                print('QueryID %s is not an active query.' % qid)

            if details and result['details'] is not None:
                sections = sorted(result['details'].keys())
                for section in sections:
                    print('%s == %s' % (section, result['details'][section]))

            if query and result['query'] is not None:
                print('%s == \n\n%s' % ('Query', result['query']))


if __name__ == '__main__':
    main()
