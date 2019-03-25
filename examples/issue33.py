#! /usr/bin/env python

import sys
import os

import logging

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco

logger = logging.getLogger()
logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
        )

ymlstr = """
k2: 222
k3:
  - done: a2
 - dtwo: b2
dthree
"""


conf = hiyapyco.load(
        ymlstr,
        os.path.join(basepath, 'olist1.yaml'),
        os.path.join(basepath, 'err.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=False
        )

print (hiyapyco.dump(conf))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

