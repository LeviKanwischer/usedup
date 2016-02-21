# -*- coding: utf-8 -*-

"""
usedup.utils
------------

This module contains the general utilities for accessing uspight.

    USAGE:
    >>> usedup.utils.Auth

See the README for further details.
"""

from configparser import ConfigParser
from getpass import getpass
import os


class Auth(object):
    """Upsight credential interactions."""
    # TODO: Research getter/setter's, as well as properties. Need to allow
    # for external file updating mid-process. This should suffice for now
    # being that a missing file will update `self.config` before assigning
    # username & password.

    def __init__(self):
        self.usedup = os.path.expanduser('~/.usedup.ini')
        self.config = self._load_config()
        self._validate_file()
        self.username = self.config['upsight']['username']
        self.password = self.config['upsight']['password']

    def _load_config(self):
        """Load & return config file."""
        config = ConfigParser()
        config.read(self.usedup)
        return config

    def _validate_file(self):
        """Verify credential file exists, create if missing."""
        if 'upsight' not in self.config:
            self.config['upsight'] = {}
            self.config['upsight']['username'] = input('Enter Username: ')
            self.config['upsight']['password'] = getpass('Enter Password: ')

        with open(self.usedup, 'w') as configfile:
            self.config.write(configfile)
