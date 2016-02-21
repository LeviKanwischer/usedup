# -*- coding: utf-8 -*-

"""
usedup.upsight
--------------

This module contains the logic for running the upsight admin functions.

    USAGE:
    >>> usedup.upsight.UsedUp

See the README for further details.
"""

import csv
import getpass
import os
import re
import sys

import requests
from requests.auth import HTTPBasicAuth

from .utils import Auth


class UsedUp(object):
    """Upsight Admin functionality."""
    _URL = r'https://analytics.upsight.com/dashboard/datamine2'

    def __init__(self):
        self.auth = HTTPBasicAuth(Auth().username, Auth().password)
        self.ADMIN = self._URL + '/admin/queries/?type=%(type)s&period=%(period)s'
        self.QUERY = self._URL + '/query/%(qid)s/'

    def _check_server(self, url):
        """Verify user has access to Upsight."""
        request = requests.get(url, auth=self.auth)
        if request.status_code != requests.status_code.ok:
            raise Error('Invalid Server Response: %s' % request.status_code)

    def history(self, period):
        """Extract past user queries."""
        # TODO: Update format handling (see alt version) & remove `download`
        periods = {'1wk': 1, '2wk': 2, '1mt': 3, '2mt': 4, '3mt': 5}
        if period not in self.periods:
            raise ValueError('%s not found in %s' % (period, periods))

        url = self.ADMIN % {'type': 'completed', 'period': periods[period]}
        self._check_server(url)

        results = requests.get(url, auth=self.auth).json()
        # TODO: sys.stdout.write() results
        header = sorted([field for field in results[0]], key=str.lower)
        raise NotImplementedError

    def running(self):
        """Currently running queries."""
        # TODO: Look into pretty console printing modules for formatting
        url = self.ADMIN % {'type': 'running', 'period': 1}
        self._check_server(url)

        line_max, join_on = 100, ''
        columns = ['User Name', 'Email Org', 'Query Type', 'Query Name',
                   'Query ID', 'Elapsed Time', 'KT Apps']
        column_max = (line_max-len(columns)*len(join_on)) // len(columns)
        results = requests.get(url, auth=self.auth).json()

        column_spaces = [i + ' '*(column_max-len(i)) for i in columns]
        sys.stdout.write(join_object.join(column_spaces))
        sys.stdout.write('-'*len(join_on.join(column_spaces)))

        for result in results:
            user = result['user_name']
            org = re.findall(r'^.*\@(.+)\..*$', result['user_email'])[0]
            query_type = result['type']
            query_name = result['query_name']
            query_id = result['id']
            elapsed = result['elapsed_time']

            query_string = re.sub(r'--.*\n', '', result['query'])
            tables = re.findall(r'((\w+)_(evt|apa|cpu|pgr|mtu))', query_string)
            tables = set(table[1] for table in tables)

            row = [user, org, query_type, query_name, query_id, elapsed, tables]
            row_strings = [str(col) for col in row]
            row_spaces = []
            for column in row_strings:
                if len(column) >= column_max:
                    column = column[:column_max-4] + '...'
                column = column + ' '*(column_max-len(column))
                row_spaces.append(column)
            sys.stdout.write(join_object.join(row_spaces))

    def kill(self, qid):
        """Cancel active query.

        `ids` == Upsight's Query ID
        """
        url = self.QUERY % qid
        self._check_server(url)

        request = requests.delete(url, auth=self.auth)
        if request.status_code == requests.status_code.no_content:
            sys.stdout.write('QueryID %s killed successfully.' % qid)

    def details(self, qid, detail, query):
        """View active query details.

        `ids` == Upsight's Query ID
        """
        # TODO: Optimize and make this printing 'pretty'
        url = self.ADMIN % {'type': 'running', 'period': 1}
        self._check_server(url)

        results = requests.get(url, auth=self.auth).json()
        results = [i for i in results if i['id'] == int(qid)]
        result = results[0] if results else None
        if detail and result:
            for item in result:
                if item != 'query':
                    sys.stdout.write(item.capitalize(), '==', result[item])
        if query and result['query']:
            sys.stdout.write('Query', '\n\n', result['query'])
