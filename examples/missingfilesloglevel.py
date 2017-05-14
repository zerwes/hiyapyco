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
        level=logging.INFO,
        format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
        )

print '*'*70
print '  hiyapyco %s' % hiyapyco.version.VERSION
print '*'*70

print '-'*70
print '  loglevelmissingfiles=logging.INFO + failonmissingfiles=True ...'
print '-'*70
try:
    conf = hiyapyco.load(
        os.path.join(basepath, 'olist1.yaml'),
        os.path.join(basepath, 'NoSuchFile.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        loglevelmissingfiles=logging.INFO
        )
except hiyapyco.HiYaPyCoInvocationException:
    pass


print '-'*70
print '  loglevelmissingfiles=logging.INFO + failonmissingfiles=False ...'
print '-'*70
conf = hiyapyco.load(
        os.path.join(basepath, 'olist1.yaml'),
        os.path.join(basepath, 'NoSuchFile.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=False,
        loglevelmissingfiles=logging.INFO
        )

print '-'*70
print '  loglevelmissingfiles=UNSET + failonmissingfiles=True ...'
print '-'*70
try:
    conf = hiyapyco.load(
        os.path.join(basepath, 'olist1.yaml'),
        os.path.join(basepath, 'NoSuchFile.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )
except hiyapyco.HiYaPyCoInvocationException:
    pass


print '-'*70
print '  loglevelmissingfiles=UNSET + failonmissingfiles=False ...'
print '-'*70
conf = hiyapyco.load(
        os.path.join(basepath, 'olist1.yaml'),
        os.path.join(basepath, 'NoSuchFile.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=False
        )
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

