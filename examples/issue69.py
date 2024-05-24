#! /usr/bin/env python

import sys
import os
import logging

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco
logger = logging.getLogger()
logging.basicConfig(
        level=logging.WARN,
        format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
        )

import yaml
yaml.Dumper.ignore_aliases = lambda *args : True

anchorbase = """
app-specs: &app-specs
  resources:
    requests:
      memory: "1"

applications:
  app1:
    <<: *app-specs
  app2:
    <<: *app-specs
"""

noanchor = """
app-specs: &app-specs
  resources:
    requests:
      memory: "1"

applications:
  app1:
    resources:
      requests:
        memory: "1"
  app2:
    resources:
      requests:
        memory: "1"
"""

anchormerge = """
applications:
  app2:
    resources:
      requests:
        memory: "2"
"""


CONF = hiyapyco.load([anchorbase, anchormerge], method=hiyapyco.METHOD_MERGE, dereferenceyamlanchors=False, mergelists=True, interpolate=True, failonmissingfiles=True)
#print (hiyapyco.dump(CONF))

print(CONF['applications']['app1']['resources']['requests']['memory'])
print(CONF['applications']['app2']['resources']['requests']['memory'])

# noanchor

#CONF = hiyapyco.load([noanchor, anchormerge], method=hiyapyco.METHOD_MERGE, mergelists=True, interpolate=True, failonmissingfiles=True)
#print (hiyapyco.dump(CONF))

#print(CONF['applications']['app1']['resources']['requests']['memory'])
#print(CONF['applications']['app2']['resources']['requests']['memory'])
