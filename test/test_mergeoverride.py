#! /usr/bin/env python

import sys
import os
import logging
import platform
import hiyapyco
import semantic_version

sys.path.insert(
        0,
        os.path.join(
            os.path.dirname(
                os.path.realpath(os.path.abspath(sys.argv[0]))
                ),
            'lib'
            )
        )
import testsetup

logger = testsetup.setup(sys.argv[1:])

basepath = os.path.dirname(os.path.realpath(__file__))

print('start test %s for hiyapyco %s using python %s (loglevel:%s)' % (
            __file__,
            hiyapyco.__version__,
            platform.python_version(),
            logging.getLevelName(logger.getEffectiveLevel())
        )
    )

logger.info('test merge override vals ...')
h = hiyapyco.HiYaPyCo(
        os.path.join(basepath, 'mo1.yaml'),
        os.path.join(basepath, 'mo2.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
        )
conf = h.data()

h.mergeprimitive = lambda a, b, context: a

t = conf['depends']
logger.info('test single val ... %s' % t)
assert t == { 'lib1': '>=2.0.0' }

try:
    conf['nosuchelement']
    raise Error
except KeyError as e:
    assert '%s' % e == '\'nosuchelement\''

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu
