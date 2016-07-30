#!/usr/bin/python

import hiyapyco
import logging

logger = logging.getLogger()
logging.basicConfig(
    level=logging.WARN,
    format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
    )
logger.setLevel(logging.DEBUG)


y1 = """
---
ml:
  - 11: 12
  - 12: 11
"""
y2 = """
---
ml:
  - 12: 12
  - 10: 10
"""


test = hiyapyco.load(y1, y2, method=hiyapyco.METHOD_MERGE, usedefaultyamlloader=True)

print test
print '.-'*10

"""test = hiyapyco.load(hiyapyco.dump(test, default_flow_style=False), y2, method=hiyapyco.METHOD_MERGE)

print test
print '.-'*10"""

