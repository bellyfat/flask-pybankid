#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_api`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-02-04

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import random
import tempfile
import json
import uuid
import unittest

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import flask

import bankid
from flask_pybankid import PyBankID


def get_random_personal_number():
    """Simple random Swedish personal number generator."""

    def _luhn_digit(id_):
        """Calculate Luhn control digit for personal number.

        Code adapted from [Faker]
        (https://github.com/joke2k/faker/blob/master/faker/providers/ssn/sv_SE/__init__.py)

        :param id_: The partial number to calculate checksum of.
        :type id_: str
        :return: Integer digit in [0, 9].
        :rtype: int

        """

        def digits_of(n):
            return [int(i) for i in str(n)]

        id_ = int(id_) * 10
        digits = digits_of(id_)
        checksum = sum(digits[-1::-2])
        for k in digits[-2::-2]:
            checksum += sum(digits_of(k * 2))
        checksum %= 10

        return checksum if checksum == 0 else 10 - checksum

    year = random.randint(1900, 2014)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    suffix = random.randint(0, 999)
    pn = "{0:04d}{1:02d}{2:02d}{3:03d}".format(year, month, day, suffix)
    return pn + str(_luhn_digit(pn[2:]))


class TestFlaskPyBankID(unittest.TestCase):
    def setUp(self):
        self.certificate_file, self.key_file = \
            bankid.create_bankid_test_server_cert_and_key(tempfile.gettempdir())

        self.app = flask.Flask('test')
        self.app.config['PYBANKID_CERT_PATH'] = self.certificate_file
        self.app.config['PYBANKID_KEY_PATH'] = self.key_file
        self.app.config['PYBANKID_TEST_SERVER'] = True
        self.context = self.app.test_request_context('/')
        self.context.push()
        self.bankid = PyBankID(self.app)

    def tearDown(self):
        self.context.pop()
        try:
            os.remove(self.certificate_file)
            os.remove(self.key_file)
        except:
            pass

    def test_authentication_and_collect(self):
        """Authenticate call and then collect with the returned orderRef UUID."""

        out = self.bankid._authenticate(get_random_personal_number())
        assert out.status_code == 200
        response_dict = json.loads(out.data.decode("utf-8"))
        # UUID.__init__ performs the UUID compliance assertion.
        assert isinstance(uuid.UUID(response_dict.get('orderRef'), version=4), uuid.UUID)
        collect_status = self.bankid._collect(response_dict.get('orderRef'))
        assert collect_status.status_code == 200
        response_dict = json.loads(collect_status.data.decode("utf-8"))
        assert response_dict.get('progressStatus') in ('OUTSTANDING_TRANSACTION', 'NO_CLIENT')

    def test_sign_and_collect(self):
        """Sign call a.nd then collect with the returned orderRef UUID."""
        # TODO: Add userVisibleData to the request that _sign reads.
        c = self.app.test_client()
        out = c.get('/sign/{0}?{1}'.format(get_random_personal_number(),
                                           urlencode(dict(userVisibleData='Text to sign'))),
                    follow_redirects=True)
        assert out.status_code == 200
        response_dict = json.loads(out.data.decode("utf-8"))
        # UUID.__init__ performs the UUID compliance assertion.
        assert isinstance(uuid.UUID(response_dict.get('orderRef'), version=4), uuid.UUID)
        collect_status = self.bankid._collect(response_dict.get('orderRef'))
        assert collect_status.status_code == 200
        response_dict = json.loads(collect_status.data.decode("utf-8"))
        assert response_dict.get('progressStatus') in ('OUTSTANDING_TRANSACTION', 'NO_CLIENT')

    def test_invalid_orderref_raises_error(self):
        out = self.bankid._collect('invalid-uuid')
        response_dict = json.loads(out.data.decode("utf-8"))
        assert out.status_code == 400
        response_dict.get('message', '').startswith("InvalidParametersError:")

    def test_already_in_progress_raises_error(self):
        pn = get_random_personal_number()
        out = self.bankid._authenticate(pn)
        response_dict = json.loads(out.data.decode("utf-8"))
        assert out.status_code == 200
        assert isinstance(uuid.UUID(response_dict.get('orderRef'), version=4), uuid.UUID)
        assert isinstance(uuid.UUID(response_dict.get('autoStartToken'), version=4), uuid.UUID)
        out2 = self.bankid._authenticate(pn)
        assert out2.status_code == 409
        response_dict = json.loads(out2.data.decode("utf-8"))
        assert response_dict.get('message', '').startswith("AlreadyInProgressError:")
