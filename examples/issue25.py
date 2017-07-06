#! /usr/bin/env python

import sys
import os

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco

base = """
key_one: 1
key_two: 2
array_of_dicts:
- dict_key_one: a
  dict_key_two: b
  dict_key_three: c
- dict_key_one: a1
  dict_key_two: b1
  dict_key_three: c1
"""
layer = """
key_two: 2222
array_of_dicts:
- dict_key_one: a2
  dict_key_two: b2
  dict_key_three: c2
"""


CONF = hiyapyco.load([base, layer], method=hiyapyco.METHOD_MERGE)
print hiyapyco.dump(CONF)

print "... using mergelists=False ..."
CONF = hiyapyco.load([base, layer], method=hiyapyco.METHOD_MERGE, mergelists=False)
print hiyapyco.dump(CONF)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

