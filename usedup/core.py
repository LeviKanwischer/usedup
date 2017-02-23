# -*- coding: utf-8 -*-

"""usedup.core

This module contains the core logic for interfacing w/ DataMine.


See the README for further details.

"""

import csv
import getpass
import logging
import math
import os
import re
import time

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

import requests
from requests.auth import HTTPBasicAuth


class UsedUp(object):
    """Basic DataMine Admin interface.

    Parameters
    ----------
    configpath : str, optional (default=None)
        Path to config file w/ login credentials.

    Attributes
    ----------
    logger : object <logging.Logger>
        Local class Logger object.
    URL : str
        Base URL path for DataMine (Upsight.com).
    ADMIN : str
        Extension URI for DataMine admin sections.
    QUERY : str
        Extension URI for DataMine query sections.
    session : object <requests.Session>
        Current session object.

    Methods
    -------
    # TODO: Complete me for public methods

    """

    URL = r'https://analytics.upsight.com/dashboard/datamine2'
    ADMIN = r'/admin/queries/?type=%(type)s&period=%(period)s'
    QUERY = r'/query/%(qid)s/'

    def __init__(self, configpath=None):
        self._classname = type(self).__name__
        self.logger = logging.getLogger(self._classname)

        self.session = requests.Session()
        self.session.auth = self._acquire_user_credentials(configpath)

    @staticmethod
    def _acquire_user_credentials(configpath=None):
        """Acquire user credentials for DataMine access.

        Parameters
        ----------
        configpath : str, optional (default=None)
            Path to config file w/ login credentials.

        Returns
        -------
        auth : object <HTTPBasicAuth>
            Authentication object w/ user credential from `requests` package.

        """
        userconfig = os.path.expanduser('~/.usedup')
        config = ConfigParser()
        config.read(userconfig)

        if configpath is not None:
            config.read(configpath)

        if 'upsight' not in config.sections():
            config['upsight'] = {}

        upsight = config['upsight']
        if 'username' in upsight and 'password' in upsight:
            username = config['upsight']['username']
            password = config['upsight']['password']

        else:
            username = input('Upsight Username: ')
            password = getpass.getpass('Upsight Password: ')

        auth = HTTPBasicAuth(username, password)
        return auth

    def _check_request_reason(self, request=None, server=None):
        """Check server status from upsight.com.

        Parameters
        ----------
        request : object <requests.Request>, optional (default=None)
            Response object from calling request on ``requests`` package.
        server : str, optional (default=self.server)
            Server URL to specific Upsight.com's BaseDatamine endpoint.

        Returns
        -------
        reason : str
            Server response (reasoning) as a status name.

        """
        server = server or self.URL
        request = request or self.session.get(server)
        reason = request.reason
        return reason

    def __enter__(self):
        """Context manager entrance method."""
        attempts, reason = 5, self._check_request_reason()
        while attempts and reason != 'OK':

            if reason == 'FORBIDDEN':
                _msg = 'User access denied, update credentials.'
                self.logger.error(_msg)
                raise requests.exceptions.ConnectionError(_msg)

            attempts -= 1
            time.sleep(5)

            reason = self._check_request_reason()

        if not attempts or reason != 'OK':
            _msg = 'Unable to successfully connect.'
            self.logger.error(_msg)
            raise requests.exceptions.ConnectionError(_msg)

        _msg = 'Successfully connected to %s' % self._classname
        self.logger.debug(_msg)

        return self

    def __exit__(self, type_, value_, trackback_):
        """Context manager exit method."""
        self.session.close()

        _msg = 'Successfully disconnected from %s' % self._classname
        self.logger.debug(_msg)

    # FIXME: Move download out of `history` method, & into CLI
    def history(self, period, outfile):
        """Extract & download list of past user queries.

        Parameters
        ----------
        period : str
            Upsight specific periods (1wk, 2wk, 1mt, 2mt, 3mt)
        outfile : str, optional (default=None)
            Desired path to download history to.

        Returns
        -------
        anonymous : boolean
            Flag for whether history data available & downloaded.

        Raises
        ------
        ValueError
            If given `period` not in available options.
        ConnectionError
            If server response is not OK.

        """
        periods = {'1wk': 1, '2wk': 2, '1mt': 3, '2mt': 4, '3mt': 5}
        if period not in periods:
            _msg = '%s not found in %s' % (period, periods)
            self.logger.error(_msg)
            raise ValueError(_msg)

        if outfile is None:
            outname = 'usedup_%sback_%s.csv'
            ts = math.floor(time.time())
            outfile = outname % (period, ts)

        params = {
            'type': 'completed',
            'period': periods[period],
        }
        url = self.URL + self.ADMIN % params

        request = self.session.get(url)
        reason = self._check_request_reason(request)

        if reason != 'OK':
            _msg = 'Server response != ok (%s)' % reason
            self.logger.error(_msg)
            raise requests.exceptions.ConnectionError(_msg)

        results = request.json()
        if not results:
            open(outfile, 'w')
            return False

        headers = sorted(results[0].keys())

        with open(outfile, 'w') as writefile:
            writer = csv.DictWriter(
                writefile,
                lineterminator='\n',
                fieldnames=headers
            )
            writer.writeheader()

            def cleaner(query):
                """Local query cleaner method."""
                query = query.lower()
                query = re.sub(r'[^\w\d\s]', '', query)
                query = re.sub(r'\s+', ' ', query)
                query = query.strip()
                return query

            # FIXME: Replace (looping) w/ proper request decoding
            for row in results:
                for col in row:

                    if col == 'query':
                        row[col] = cleaner(row[col])

                try:
                    writer.writerow(row)
                except UnicodeEncodeError as _except:
                    _msg = str(_except)
                    self.logger.error(_msg)

        return True

    def kill(self, qid):
        """Submit a cancellation request for a DataMine query.

        Parameters
        ----------
        qid : str
            DataMine Query ID of query to cancel.

        Returns
        -------
        result : boolean
            Query cancellation status.

        """
        params = {
            'qid': qid,
        }
        url = self.URL + self.QUERY % params
        request = self.session.delete(url)

        if request.status_code != requests.codes.no_content:
            _msg = 'QueryID %s failed to cancel.' % qid
            self.logger.error(_msg)
            result = False

        else:
            _msg = 'QueryID %s canceled successfully.' % qid
            self.logger.info(_msg)
            result = True

        return result

    def running(self):
        """Fetch details about all running queries on DataMine.

        Returns
        -------
        queries : array-like <list> of <dict>
            List of running queries w/ details.

        """
        params = {
            'type': 'running',
            'period': 1,
        }
        url = self.URL + self.ADMIN % params
        request = self.session.get(url)

        reason = self._check_request_reason(request)
        if reason != 'OK':
            _msg = 'Server response != ok (%s)' % reason
            self.logger.error(_msg)
            raise requests.exceptions.ConnectionError(_msg)

        results = request.json()

        queries = []
        for result in results:
            query = {}
            query['User Name'] = result['user_name']
            query['Email Domain'] = re.sub('^[^@]+@', '', result['user_email'])
            query['Query Type'] = result['type']
            query['Query Name'] = result['query_name']
            query['Query ID'] = result['id']
            query['Elapsed Time'] = result['elapsed_time']

            _query = re.sub(r'--.*\n', '', result['query'])
            _apps = re.findall(r'((\w+)_(evt|apa|cpu|pgr|mtu))', _query)
            query['KT Apps'] = set(app[1] for app in _apps)

            queries.append(query)

        return queries

    def status(self, qid, details=True, query=True):
        """Fetch details & status about an active query on DataMine.

        Parameters
        ----------
        qid : str
            DataMine Query ID of query to cancel.
        details : boolean, optional (default=True)
            Flag for returning query status details.
        query : boolean, optional (default=False)
            Flag for returning query string details.

        Returns
        -------
        status : array-like <dict>
            Dict of query status information.

        """
        params = {
            'type': 'running',
            'period': 1,
        }
        url = self.URL + self.ADMIN % params
        request = self.session.get(url)

        reason = self._check_request_reason(request)
        if reason != 'OK':
            _msg = 'Server response != ok (%s)' % reason
            self.logger.error(_msg)
            raise requests.exceptions.ConnectionError(_msg)

        results = request.json()
        records = [record for record in results if record['id'] == int(qid)]
        record = records[0] if records else None

        if record is None:
            return None

        status = {'details': None, 'query': None}

        if details:
            status['details'] = {}
            for item in record:
                if item != 'query':
                    status['details'][item] = record[item]

        if query:
            status['query'] = record['query']

        return status
