# -*- coding: utf-8 -*-

"""
usedup.usedup
-------------

This module contains the logic for running the upsight admin functions.

    USAGE:
    >>> usedup.usedup.UsedUp

See the README.txt for further details.
"""

import os
import sys
import re
import csv
import getpass
import requests


URL = 'https://analytics.upsight.com/dashboard/datamine2'


def get_credentials():
    """Get & Encode credentials for Upsight authorization."""
    username = input('Upsight Username: ')
    password = getpass.getpass('Upsight Password: ')
    return requests.auth.HTTPBasicAuth(username, password)


class UsedUp(object):
    """Maintain logic for running Upsight admin tasks."""

    def __init__(self):
        self.admin_url = URL + '/admin/queries/?type={type}&period={period}'
        self.query_url = URL + '/query/{query_id}/'
        self.periods = {'1wk': 1, '2wk': 2, '1mt': 3, '2mt': 4, '3mt': 5}
        self.auth = get_credentials()

    def _check_server(self, url):
        """Verify access to Upsight, provide logic on Fail."""
        request = requests.get(url, auth=self.auth)
        if str(request.status_code)[0] == '4':
            print('Incorrect credentials, please re-enter...')
            self.auth = get_credentials()
            self._check_server(url)
        elif str(request.status_code)[0] == '5':
            print('Server not available.')
            sys.exit(1)

    def history(self, period, outfile):
        """Download an archive of previously run queries."""
        if period not in self.periods:
            period = '1wk'

        if not outfile:
            downloads = os.path.expanduser('~/downloads')
            outfile = os.path.join(downloads, 'usedup_{}.csv'.format(period))

        period = self.periods[period]
        url = self.admin_url.format(type='completed', period=period)
        self._check_server(url)

        results = requests.get(url, auth=self.auth).json()
        header = sorted([field for field in results[0]], key=str.lower)
        with open(outfile, 'w') as f_out:
            writer = csv.DictWriter(f_out, lineterminator='\n', fieldnames=header)
            writer.writeheader()
            writer.writerows(results)

    def running(self):
        """Return list of currently running queries."""
        url = self.admin_url.format(type='running', period=1)
        self._check_server(url)

        results = requests.get(url, auth=self.auth).json()
        columns = ['User Name', 'Email Org', 'Query Type', 'Query Name',
                   'Query ID', 'Elapsed Time', 'KT Apps']
        max_line, join_object = 100, ''
        column_max = (max_line-len(columns)*len(join_object)) // len(columns)

        column_spaces = [i + ' '*(column_max-len(i)) for i in columns]
        print(join_object.join(column_spaces))
        print('-'*len(join_object.join(column_spaces)))

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
            print(join_object.join(row_spaces))

    def kill(self, query_id):
        """Kill actively running query."""
        url = self.query_url.format(query_id=query_id)
        self._check_server(url)

        request = requests.delete(url, auth=self.auth)
        if request.status_code == 204:
            print('QueryID {} killed successfully.'.format(query_id))

    def details(self, query_id, detail, query):
        """Return details about active query."""
        # TODO: Optimize and make this printing 'pretty'
        url = self.admin_url.format(type='running', period=1)
        self._check_server(url)

        results = requests.get(url, auth=self.auth).json()
        results = [i for i in results if i['id'] == int(query_id)]
        result = results[0] if results else None
        if result:
            if detail:
                for item in result:
                    if item != 'query':
                        print(item.capitalize(), '==', result[item])
            if query and result['query']:
                print('Query', '\n\n', result['query'])
        else:
            print('Query must be active to view details...')
