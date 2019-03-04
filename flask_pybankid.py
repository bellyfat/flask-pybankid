#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
flask_pybankid  -- Flask Extension for PyBankID
===============================================

Created by hbldh <henrik.blidh@nedomkull.com>

Created on 2015-11-19

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

from flask import current_app, jsonify, request
from bankid import BankIDClient, BankIDJSONClient, exceptions

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class PyBankID(object):
    """The class handling the PyBankID client.

    It can be used when initiating the Flask app:

    .. code-block:: python

        from flask import Flask
        from flask_pybankid import PyBankID

        app = Flask(__name__)
        bankid = PyBankID(app)

    Configuration of the BankID client is done via parameters to Flask:

    .. code-block:: python

        PYBANKID_CERT_PATH = 'path/to/certificate.pem'
        PYBANKID_KEY_PATH = 'path/to/key.pem'
        PYBANKID_TEST_SERVER = True

    Should several BankID clients with different settings be desired, one
    can change the prefix `PYBANKID` to an arbitrarily chosen prefix instead,
    and initiate the :class:`~PyBankID` extension with the extra
    keyword `config_prefix='MY_PREFIX'`

    """

    def __init__(self, app=None, config_prefix="PYBANKID"):
        self.config_prefix = config_prefix
        self.app = app
        if app is not None:
            self.init_app(app, config_prefix)

    def init_app(self, app, config_prefix="PYBANKID"):
        """Initialize the `app` for use with this :class:`~PyBankID`. This is
        called automatically if `app` is passed to :meth:`~PyBankID.__init__`.

        The app is configured according to the configuration variables
        ``PREFIX_CERT_PATH``, ``PREFIX_KEY_PATH`` and ``PREFIX_TEST_SERVER``,
         where "PREFIX" defaults to "PYBANKID".

        :param flask.Flask app: the application to configure for use with
           this :class:`~PyBankID`
        :param str config_prefix: determines the set of configuration
           variables used to configure this :class:`~PyBankID`.

        """
        if "pybankid" not in app.extensions:
            app.extensions["pybankid"] = {}

        if config_prefix in app.extensions["pybankid"]:
            raise Exception('duplicate config_prefix "{0}"'.format(config_prefix))

        app.config.setdefault(self._config_key("CERT_PATH"), "")
        app.config.setdefault(self._config_key("KEY_PATH"), "")
        app.config.setdefault(self._config_key("TEST_SERVER"), False)

        # Adding the three url endpoints.
        app.add_url_rule(
            "/authenticate/<personal_number>", view_func=self._authenticate
        )
        app.add_url_rule("/sign/<personal_number>", view_func=self._sign)
        app.add_url_rule("/collect/<order_ref>", view_func=self._collect)

        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def _config_key(self, suffix):
        return "{0}_{1}".format(self.config_prefix, suffix)

    def teardown(self, exception):
        pass

    @property
    def client(self):
        """The automatically created :py:class:`bankid.client.BankIDClient` object.

        :return: The BankID client.
        :rtype: :py:class:`bankid.jsonclient.BankIDJSONClient`

        """
        ctx = stack.top
        attr_name = self._config_key("client")
        if ctx is not None:
            if not hasattr(ctx, attr_name):
                setattr(
                    ctx,
                    attr_name,
                    BankIDClient(
                        (
                            current_app.config.get(self._config_key("CERT_PATH")),
                            current_app.config.get(self._config_key("KEY_PATH")),
                        ),
                        current_app.config.get(self._config_key("TEST_SERVER")),
                    ),
                )
            return getattr(ctx, attr_name)

    def _authenticate(self, personal_number):
        try:
            response = self.client.authenticate(personal_number)
        except exceptions.BankIDError as e:
            return self.handle_exception(
                FlaskPyBankIDError.create_from_pybankid_exception(e)
            )
        except Exception as e:
            return self.handle_exception(FlaskPyBankIDError(str(e), 500))
        else:
            return jsonify(**response)

    def _sign(self, personal_number):
        text_to_sign = request.args.get("userVisibleData", "")
        try:
            response = self.client.sign(text_to_sign, personal_number)
        except exceptions.BankIDError as e:
            return self.handle_exception(
                FlaskPyBankIDError.create_from_pybankid_exception(e)
            )
        except Exception as e:
            return self.handle_exception(FlaskPyBankIDError(str(e), 500))
        else:
            return jsonify(**response)

    def _collect(self, order_ref):
        try:
            response = self.client.collect(order_ref)
        except exceptions.BankIDError as e:
            return self.handle_exception(
                FlaskPyBankIDError.create_from_pybankid_exception(e)
            )
        except Exception as e:
            return self.handle_exception(FlaskPyBankIDError(str(e), 500))
        else:
            return jsonify(**response)

    @staticmethod
    def handle_exception(error):
        """Simple method for handling exceptions raised by `PyBankID`.

        :param flask_pybankid.FlaskPyBankIDError error: The exception to handle.
        :return: The exception represented as a dictionary.
        :rtype: dict

        """
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


class FlaskPyBankIDError(Exception):
    """An exception wrapper to handle error output to JSON in a simple way."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    @classmethod
    def create_from_pybankid_exception(cls, exception):
        """Class method for initiating from a `PyBankID` exception.

        :param bankid.exceptions.BankIDError exception:
        :return: The wrapped exception.
        :rtype: :py:class:`~FlaskPyBankIDError`

        """
        return cls(
            "{0}: {1}".format(exception.__class__.__name__, str(exception)),
            _exception_class_to_status_code.get(exception.__class__),
        )

    def to_dict(self):
        """Create a dict representation of this exception.

        :return: The dictionary representation.
        :rtype: dict

        """
        rv = dict(self.payload or ())
        rv["message"] = self.message
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
