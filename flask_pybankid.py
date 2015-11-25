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
from bankid import BankIDClient, exceptions

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class PyBankID(object):

    def __init__(self, app=None, config_prefix='PYBANKID'):
        self.app = app
        if app is not None:
            self.init_app(app, config_prefix)

    def init_app(self, app, config_prefix='PYBANKID'):
        if 'pybankid' not in app.extensions:
            app.extensions['pybankid'] = {}

        if config_prefix in app.extensions['pybankid']:
            raise Exception('duplicate config_prefix "{0}"'.format(config_prefix))

        self.config_prefix = config_prefix
        app.config.setdefault(self._config_key('CERT_PATH'), '')
        app.config.setdefault(self._config_key('KEY_PATH'), '')
        app.config.setdefault(self._config_key('TEST_SERVER'), False)

        # Adding the three url endpoints.
        app.add_url_rule("/authenticate/<personal_number>", view_func=self._authenticate)
        app.add_url_rule("/sign/<personal_number>", view_func=self._sign)
        app.add_url_rule("/collect/<order_ref>", view_func=self._collect)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def _config_key(self, suffix):
        return '{0}_{1}'.format(self.config_prefix, suffix)

    def teardown(self, exception):
        pass

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
        try:
            response = self.client.authenticate(personal_number)
        except exceptions.BankIDError as e:
            return self.handle_exception(FlaskPyBankIDError.create_from_pybankid_exception(e))
        except Exception as e:
            return self.handle_exception(FlaskPyBankIDError(str(e), 500))
        else:
            return jsonify(**response)

    def _sign(self, personal_number):
        text_to_sign = request.args.get('text', '')
        try:
            response = self.client.sign(text_to_sign.encode('utf8'), personal_number)
        except exceptions.BankIDError as e:
            return self.handle_exception(FlaskPyBankIDError.create_from_pybankid_exception(e))
        except Exception as e:
            return self.handle_exception(FlaskPyBankIDError(str(e), 500))
        else:
            return jsonify(**response)

    def _collect(self, order_ref):
        try:
            response = self.client.collect(order_ref)
        except exceptions.BankIDError as e:
            return self.handle_exception(
                FlaskPyBankIDError.create_from_pybankid_exception(e))
        except Exception as e:
            return self.handle_exception(FlaskPyBankIDError(str(e), 500))
        else:
            return jsonify(**response)

    @staticmethod
    def handle_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


class FlaskPyBankIDError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    @classmethod
    def create_from_pybankid_exception(cls, exception):
        return cls("{0}: {1}".format(
            exception.__class__.__name__, exception.message),
            _exception_class_to_status_code.get(exception.__class__))

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

_exception_class_to_status_code = {
    exceptions.AlreadyInProgressError: 409,
    exceptions.AccessDeniedRPError: 403,
    exceptions.CancelledError: 409,
    exceptions.UserCancelError: 409,
    exceptions.CertificateError: 403,
    exceptions.StartFailedError: 404,
    exceptions.ExpiredTransactionError: 408,
    exceptions.ClientError: 500,
    exceptions.RetryError: 500,
    exceptions.InternalError: 500,
    exceptions.InvalidParametersError: 400,

}
