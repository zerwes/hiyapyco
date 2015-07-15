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

logger.info('test simple vals ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'base.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )

t = conf['singel']
logger.info('test single val ... %s' % t)
assert t == 'base'

t = conf['int']
logger.info('test int val ... %s' % t)
assert t == 1

t = conf['array']
logger.info('test list val ... %s' % t)
assert t == ['base1', 'base2']

t = conf['hash']
logger.info('test simple dict ... %s' % t)
assert t == {'k1': 'b1', 'k2': 'b2'}

t = conf['deeplist']
logger.info('test deeplist ... %s' % t)
assert t == [{'d1': {'d1k1': 'v1', 'd1k2': 'v2'}}, {'d2': {'d2k2': 'x2', 'd2k1': 'x1'}}, {'d32': {'a': 'A2', 'b': 'B2'}, 'd31': {'a': 'A', 'c': 'C', 'b': 'B'}}]

t = conf['deepmap']
logger.info('test deepmap ... %s' % t)
assert t == {'l1k1' : {'l2k1': 'xyz', 'l2k2': 'abc'}, 'l1k2': {'l2k1': 'bli', 'l2k2': 'bla', 'l2k3': 'blub'}}

t = conf.get('nosuchelement', 'default value')
logger.info('test default value ... %s' % t)
assert t == 'default value'

try:
    conf['nosuchelement']
    raise Error
except KeyError as e:
    assert '%s' % e == '\'nosuchelement\''


print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

