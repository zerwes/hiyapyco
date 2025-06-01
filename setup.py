#!/usr/bin/env python

import sys
import os

from setuptools import setup

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

HIYAPYCOVERSION='0.7.0'

long_description = open('README.rst').read()

installrequires = [
    'PyYAML<7',
    'Jinja2>3,<4',
    'MarkupSafe<4'
    ]

setup(name='HiYaPyCo',
    version=HIYAPYCOVERSION,
    description='Hierarchical Yaml Python Config',
    long_description="%s" % long_description,
    long_description_content_type='text/x-rst',
    author='Klaus Zerwes zero-sys.net',
    author_email='zerwes@users.noreply.github.com',
    url='https://github.com/zerwes/hiyapyco',
    license='GPL-3.0-or-later',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: File Formats',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
    ],
    packages=['hiyapyco'],
    keywords=['configuration', 'parser', 'yaml'],
    install_requires = installrequires,
    platforms = 'any',
    )

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu
