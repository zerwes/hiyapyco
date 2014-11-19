#! /usr/bin/env python

import sys
import os
import logging

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco

print('='*10, 'method=hiyapyco.METHOD_SIMPLE', '='*10)

conf = hiyapyco.load(
        os.path.join(basepath, 'list1.yaml'),
        os.path.join(basepath, 'list2.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )
print(conf)
print('-'*10, 'YAML', '-'*10)
print(hiyapyco.dump(conf))

print('='*10, 'method=hiyapyco.METHOD_MERGE', '='*10)

conf = hiyapyco.load(
        os.path.join(basepath, 'list1.yaml'),
        os.path.join(basepath, 'list2.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
        )
print(conf)
print('-'*10, 'YAML', '-'*10)
print(hiyapyco.dump(conf))
assert conf == {'l': {'a': ['laa', 'lab', 'lac', 'lad'], 'b': ['lba', 'lbb', 'lcc', 'lbd'], 'c': [{'csub': ['lcc1', 'lcc2', 'lcc4', 'lcc5']}, 'lcc 2 only', {'csub2': ['csub2 1', 'csub2 2']}, 'lca', 'lcb', 'lcc', 'lcd']}}

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

