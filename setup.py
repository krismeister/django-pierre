#!/usr/bin/env python

import os
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup

version = '1.0'

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
    "Environment :: Web Environment",
    "Framework :: Django",
]

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'

setup(
    name='django-pierre',
    version=version,
    url='http://code.google.com/p/django-pierre/',
    author='James Stevenson',
    author_email='',
    license='Apache License 2.0',
    package_dir={'pierre': 'pierre'},
    description='Useful Django utilities',
    classifiers=classifiers
)

