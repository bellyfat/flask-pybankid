#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask-PyBankID
--------------

A Flask tool for using PyBankID on your site.
"""

from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals
from __future__ import absolute_import

from setuptools import setup


setup(
    name='Flask-PyBankID',
    version='1.0',
    url='https://github.com/hbldh/flask-pybankid/',
    license='MIT',
    author='Henrik Blidh',
    author_email='henrik.blidh@nedomkull.com',
    description='Flask Extension for BankID client',
    long_description=__doc__,
    packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'pybankid>=0.3.0',
        'requests>=2.7.0',
        'suds-jurko>=0.6',
        'six>=1.9.0'
    ],
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



