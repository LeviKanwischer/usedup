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

from usedup.core import UsedUp


__title__ = 'usedup'
__version__ = '2.0.0'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2016 Levi Kanwischer'
__author__ = 'Levi Kanwischer'
__maintainer__ = 'Levi Kanwischer'
__email__ = 'levi@kanwischer.me'
__all__ = [
    '__version__',
    '__license__',
    '__email__',

    'UsedUp',
]
