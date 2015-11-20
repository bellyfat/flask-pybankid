#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py
===========

hbldh <henrik.blidh@nedomkull.com>
Created on 2015-11-19

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from flask import current_app, jsonify, request
from bankid import BankIDClient


# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class PyBankID(object):

    def __init__(self, app=None):
        self.app = app
        self.config_prefix = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app, config_prefix='PYBANKID'):
        if 'pybankid' not in app.extensions:
            app.extensions['pybankid'] = {}

        if config_prefix in app.extensions['pybankid']:
            raise Exception('duplicate config_prefix "{0}"'.format(config_prefix))

        self.config_prefix = config_prefix
        app.config.setdefault(self._config_key('CERT_PATH'), '')
        app.config.setdefault(self._config_key('KEY_PATH'), '')
        app.config.setdefault(self._config_key('TEST_SERVER'), False)

        app.add_url_rule("/authenticate/<personal_number>", view_func=self._authenticate)
        app.add_url_rule("/sign/<personal_number>", view_func=self._sign)
        app.add_url_rule("/collect/<order_ref>", view_func=self._collect)

        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def _config_key(self, suffix):
        return '{0}_{1}'.format(self.config_prefix, suffix)

    def teardown(self, exception):
        ctx = stack.top
        attr_name = self._config_key('client')
        if hasattr(ctx, attr_name):
            getattr(ctx, attr_name).close()

    @property
    def client(self):
        ctx = stack.top
        attr_name = self._config_key('client')
        if ctx is not None:
            if not hasattr(ctx, attr_name):
                setattr(ctx, attr_name, BankIDClient(
                    (current_app.config.get(self._config_key('CERT_PATH')),
                     current_app.config.get(self._config_key('KEY_PATH'))),
                    current_app.config.get(self._config_key('TEST_SERVER'))))
            return getattr(ctx, attr_name)

    def _authenticate(self, personal_number):
        return jsonify(**self.client.authenticate(personal_number))

    def _sign(self, personal_number):
        text_to_sign = request.args.get('text', '')
        return jsonify(**self.client.sign(text_to_sign, personal_number))

    def _collect(self, order_ref):
        return jsonify(**self.client.collect(order_ref))
