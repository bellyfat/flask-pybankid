#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask-PyBankID
-------------

A Flask tool for using `PyBankID <https://github.com/hbldh/pybankid>`_ on your site.

Installation
============

Flask-PyBankID is pip-installable:

    pip install Flask-PyBankID

You can install the latest development snapshot like so:

    pip install https://github.com/hbldh/flask-pybankid/tarball/master#egg=Flask-PyBankID

Development
===========

Source code is hosted in `GitHub <https://github.com/hbldh/flask-pybankid>`_.

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import sys
from setuptools import setup

# Get the long description from the README file
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst')) as f:
        long_description = f.read()
except:
    long_description = __doc__

setup(
    name='Flask-PyBankID',
    version='0.1.2rc1',
    url='https://github.com/hbldh/flask-pybankid/',
    license='MIT',
    author='Henrik Blidh',
    author_email='henrik.blidh@nedomkull.com',
    description='Flask Extension for PyBankID client',
    long_description=long_description,
    py_modules=['flask_pybankid'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
        'pybankid>=0.3.4'
    ],
    test_suite="tests",
    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)



