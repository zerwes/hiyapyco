#! /usr/bin/env python

import sys
import os
import logging
import platform
import hiyapyco

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

logger.info('test multiple yaml in one file w/ original yaml loader ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'multiple.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        usedefaultyamlloader=True
        )

t = conf['a']
logger.info('test single val ... %s' % t)
assert t == 'xxx'

t = conf['b']
logger.info('test single val ... %s' % t)
assert t == 'bbb'

t = conf['d']
logger.info('test dict val ... %s' % t)
assert t == {'a' : 'x', 'z' : 'z'}


logger.info('test multiple yaml in one file w/ odyldo ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'multiple.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        usedefaultyamlloader=False
        )

t = conf['a']
logger.info('test single val ... %s' % t)
assert t == 'xxx'

t = conf['b']
logger.info('test single val ... %s' % t)
assert t == 'bbb'

t = conf['d']
logger.info('test dict val ... %s' % t)
assert t == {'a' : 'x', 'z' : 'z'}

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

