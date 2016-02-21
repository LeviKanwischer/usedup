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

from .upsight import UsedUp


__title__ = 'usedup'
__version__ = '1.0.0b1'
__author__ = 'Levi Kanwischer'
__copyright__ = 'Copyright (c) 2016 Levi Kanwischer'
__license__ = 'MIT'
__all__ = ['UsedUp']
