#!/usr/bin/env python

import sys
import os

from setuptools import setup

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))
from hiyapyco import __version__ as hiyapycoversion


long_description='A simple python lib allowing hierarchical overlay of config files in YAML syntax, offering different merge methods and variable interpolation based on jinja2'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(name='HiYaPyCo',
    version=hiyapycoversion,
    description='Hierarchical Yaml Python Config',
    long_description="%s" % long_description,
    author='Klaus Zerwes zero-sys.net',
    author_email='zerwes@users.noreply.github.com',
    url='https://github.com/zerwes/hiyapyco',
    license='LGPL',
    classifiers=[	
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
    ],
    packages=['hiyapyco'],
    keywords='configuration parser yaml',
    install_requires = ['PyYAML', 'Jinja2',],
    platforms = 'any',
    )

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

