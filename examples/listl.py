#! /usr/bin/env python

import sys
import os
import logging
import pprint

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))
import hiyapyco

logger = logging.getLogger()
logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
        )

conf = hiyapyco.load(
        os.path.join(basepath, 'listl1.yaml'),
        os.path.join(basepath, 'listl2.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
        )
print('-'*10, 'DATA', '-'*10)
print(conf)
print('-'*10, 'PPRINT', '-'*10)
pprint.PrettyPrinter(indent=4).pprint(conf)
print('-'*10, 'YAML', '-'*10)
print(hiyapyco.dump(conf))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

