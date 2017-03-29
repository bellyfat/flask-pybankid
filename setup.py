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

from codecs import open
from setuptools import setup


def read(f):
    return open(f, encoding='utf-8').read()

setup(
    name='Flask-PyBankID',
    version='0.3.0',
    url='https://github.com/hbldh/flask-pybankid/',
    license='MIT',
    author='Henrik Blidh',
    author_email='henrik.blidh@nedomkull.com',
    description='Flask Extension for PyBankID client',
    long_description=read('README.rst'),
    py_modules=['flask_pybankid'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=read('requirements.txt').strip().splitlines(),
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Security',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)



