#! /usr/bin/env python

import sys
import os
import logging

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco

base = """
undeftype1: stringish1
undeftype2: stringish2
undeftype3: stringish3
"""
layer = """
undeftype1:
    - listelem1
    - listelem2
undeftype2:
    k1: elem1
    k2: elem2
undeftype3: newstring
"""

logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
    )

CONF = hiyapyco.load([base, layer], method=hiyapyco.METHOD_MERGE)
print (hiyapyco.dump(CONF))

print ("... using mergelists=False ...")
CONF = hiyapyco.load([base, layer], method=hiyapyco.METHOD_MERGE, mergelists=False)
print (hiyapyco.dump(CONF))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu
