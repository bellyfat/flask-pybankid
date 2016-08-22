Flask-PyBankID
==============

.. image:: https://travis-ci.org/hbldh/flask-pybankid.svg?branch=master
    :target: https://travis-ci.org/hbldh/flask-pybankid
.. image:: https://readthedocs.org/projects/flask-pybankid/badge/?version=latest
    :target: http://flask-pybankid.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: http://img.shields.io/pypi/v/Flask-PyBankID.svg
    :target: https://pypi.python.org/pypi/Flask-PyBankID/
.. image:: https://coveralls.io/repos/github/hbldh/flask-pybankid/badge.svg?branch=master
    :target: https://coveralls.io/github/hbldh/flask-pybankid?branch=master

A Flask extension for using `PyBankID <https://github.com/hbldh/pybankid>`_ on your site.

An `example web application using PyBankID and Flask-PyBankID <https://github.com/hbldh/pybankid-example-app>`_
exists and can be found in deployed state on `Heroku <https://bankid-example-app.herokuapp.com/>`_.

Installation
------------

Flask-PyBankID is pip-installable:

.. code-block:: bash

    $ pip install Flask-PyBankID

You can install the latest development snapshot like so:

.. code-block:: bash

    $ pip install https://github.com/hbldh/flask-pybankid/tarball/master#egg=Flask-PyBankID

Development
-----------

Source code is hosted in `GitHub <https://github.com/hbldh/flask-pybankid>`_.


Usage
-----

The `Flask-PyBankID` package adds a `PyBankID` class that can be used when initiating the Flask app:

.. code-block:: python

    from flask import Flask
    from flask_pybankid import PyBankID

    app = Flask(__name__)
    bankid = PyBankID(app)

Configuration of the BankID client is done via the regular parameters to Flask:

.. code-block:: python

    PYBANKID_CERT_PATH = 'path/to/certificate.pem'
    PYBANKID_KEY_PATH = 'path/to/key.pem'
    PYBANKID_TEST_SERVER = True

Should several BankID clients with different settings be desired, one
can change the prefix `PYBANKID` to an arbitrarily chosen prefix instead,
and initiate the `PyBankID` extension with the extra keyword `config_prefix='MY_PREFIX'`

The PyBankID wrapper adds three API endpoints for your site, all accepting `GET` requests:

* `/authenticate/YYYYMMDDXXXX`
    - Initiate a BankID authentication session.
* `/sign/YYYYMMDDXXXX`
    - Initiate a BankID signing session (requires data to be sent in as well; see below).
* `/collect/<orderRef>`
    - Collect the signing status of a session with the sent in order reference UUID.

These endpoints can then be called either from the backend or the frontend. Here are some
`jquery ajax <https://api.jquery.com/jquery.ajax/>`_ examples for frontend use:

Authenticate example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    function authenticate(nationalIDNumber) {
        $.ajax({
            type: "GET",
            url: "/authenticate/" + nationalIDNumber,
            error: function(xhr, statusText) {
                console.log(xhr.responseJSON.message);
                return {};
            },
            success: function(data){
                return data;
            }
        });
    });

Sign example
~~~~~~~~~~~~

.. code-block:: javascript

    function sign(nationalIDNumber, userVisibleData) {
        $.ajax({
            type: "GET",
            url: "/sign/" + nationalIDNumber,
            data: { 'userVisibleData': 'Signera med Personnummer: ' + nationalIDNumber },
            error: function(xhr, statusText) {
                console.log(xhr.responseJSON.message);
                return {};
            },
            success: function(data){
                return data;
            }
        });
    });

Collect example
~~~~~~~~~~~~~~~

.. code-block:: javascript

    function collect(orderRef) {
        $.ajax({
            type: "GET",
            url: "/collect/" + orderRef,
            error: function(xhr, statusText) {
                console.log(xhr.responseJSON.message);
                return {};
            },
            success: function(data){
                return data;
            }
        });
    });

Testing
-------

The Flask-PyBankID solution can be tested as such:

.. code-block:: bash

    python setup.py test

or by using `pytest`:

.. code-block:: bash

    py.test tests/

More Info
---------

* `BankID information for Relying Partner <https://www.bankid.com/bankid-i-dina-tjanster/rp-info>`_
