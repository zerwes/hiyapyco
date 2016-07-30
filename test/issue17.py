#!/usr/bin/python

import hiyapyco
import logging
import sys

logger = logging.getLogger()
logging.basicConfig(
    level=logging.WARN,
    format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
    )
logger.setLevel(logging.DEBUG)


test = "\n"

for a in range(11, 13):
    number_a = a
    for b in range(11, 13):
        number_b = b
        new = hiyapyco.dump([{number_a: number_b}])
        print new
        merged = hiyapyco.load(test, new, method=hiyapyco.METHOD_MERGE)
        test = hiyapyco.dump(merged, default_flow_style=False)
        print test
        print '.-'*10

