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

from .upsight import UsedUp


__title__ = 'usedup'
__version__ = '1.0.0b1'
__author__ = 'Levi Kanwischer'
__copyright__ = 'Copyright (c) 2016 Levi Kanwischer'
__license__ = 'MIT'
__all__ = ['UsedUp']
