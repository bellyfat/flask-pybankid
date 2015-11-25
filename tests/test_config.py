#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_config`
==================

Created by hbldh <henrik.blidh@nedomkull.com>
Created on 2016-02-04

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import tempfile
import unittest

import flask

import bankid
from flask_pybankid import PyBankID



class FlaskPyMongoConfigTest(unittest.TestCase):

    def setUp(self):
        self.certificate_file, self.key_file = \
            bankid.create_bankid_test_server_cert_and_key(tempfile.gettempdir())

        self.app = flask.Flask('test')
        self.context = self.app.test_request_context('/')
        self.context.push()


    def tearDown(self):
        self.context.pop()
        try:
            os.remove(self.certificate_file)
            os.remove(self.key_file)
        except:
            pass

    def test_default_config_prefix(self):
        self.app.config['PYBANKID_CERT_PATH'] = self.certificate_file
        self.app.config['PYBANKID_KEY_PATH'] = self.key_file
        self.app.config['PYBANKID_TEST_SERVER'] = True

        fbid = PyBankID(self.app)

        assert fbid.client.certs == (self.certificate_file, self.key_file)
        assert fbid.client.api_url == 'https://appapi.test.bankid.com/rp/v4'

    def test_custom_config_prefix(self):
        self.app.config['CUSTOM_CERT_PATH'] = self.certificate_file
        self.app.config['CUSTOM_KEY_PATH'] = self.key_file
        self.app.config['CUSTOM_TEST_SERVER'] = True

        fbid = PyBankID(self.app, 'CUSTOM')

        assert fbid.client.certs == (self.certificate_file, self.key_file)
        assert fbid.client.api_url == 'https://appapi.test.bankid.com/rp/v4'
