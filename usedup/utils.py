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
    """Handle Upsight credential interactions."""
    # TODO: Research getter/setter's, as well as properties. Need to allow
    # for external file updating mid-process. This should suffice for now
    # being that a missing file will update `self.config` before assigning
    # username & password

    def __init__(self):
        self.usedup = os.path.expanduser('~/.usedup')
        self.config = self._load_config()
        self._validate_file()
        self.username = self.config['upsight']['username']
        self.password = self.config['upsight']['password']

    def _load_config(self):
        """Load & return config file."""
        config = ConfigParser()
        return config.read(self.usedup)

    def _validate_file(self):
        """Verify credential file exists, create if missing."""
        if not 'upsight' in self.config:
            config['upsight'] = {}
            config['elapsed']['username'] = input('Enter Username: ')
            config['upsight']['password'] = getpass('Enter Password: ')

        with open(self.usedup, 'w') as configfile:
            configfile.write(config)

