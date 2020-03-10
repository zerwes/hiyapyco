#!/usr/bin/env python

import sys
import os

from setuptools import setup

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

hiyapycoversion='0.4.16'

long_description = open('README.rst').read()

installrequires = ['PyYAML', 'Jinja2>1,<3',]

try:
    from collections import OrderedDict
except ImportError:
    installrequires.append('ordereddict')

setup(name='HiYaPyCo',
    version=hiyapycoversion,
    description='Hierarchical Yaml Python Config',
    long_description="%s" % long_description,
    author='Klaus Zerwes zero-sys.net',
    author_email='zerwes@users.noreply.github.com',
    url='https://github.com/zerwes/hiyapyco',
    license='GPL',
    classifiers=[	
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    packages=['hiyapyco'],
    keywords='configuration parser yaml',
    install_requires = installrequires,
    platforms = 'any',
    )

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

