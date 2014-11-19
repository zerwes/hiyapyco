#! /usr/bin/env python

import sys
import os
import logging

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))
import hiyapyco

conf = hiyapyco.load(
        os.path.join(basepath, 'listn1.yaml'),
        os.path.join(basepath, 'listn2.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
        )
print(conf)
print('-'*10, 'YAML', '-'*10)
print(hiyapyco.dump(conf))
assert conf == {'l1': [{'d1': {'d1k1': 'v1', 'd1k2': 'v2', 'd1k3': 'v3'}}, {'d2': {'d2k2': 'x2', 'd2k1': 'xxx'}}, {'d0': {'d0k1': 'only in 1'}}, {'d3': {'d3k1': 'only in 2'}}]}

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

