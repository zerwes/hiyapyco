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

logger.info('test substitute vals ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'base.yaml'),
        os.path.join(basepath, 'baseext.yaml'),
        method=hiyapyco.METHOD_SUBSTITUTE,
        failonmissingfiles=True
        )

t = conf['singel']
logger.info('test single val ... %s' % t)
assert t == 'ext'

t = conf['int']
logger.info('test int val ... %s' % t)
assert t == 10

t = conf['array']
logger.info('test list val ... %s' % t)
assert t == ['base1', 'base2', 'baseext1', 'baseext2']

t = conf['hash']
logger.info('test simple dict ... %s' % t)
assert t == {'k1': 'b1', 'k2': 'b2', 'ek1': 'be1', 'ek2': 'be2'}

t = conf['deeplist']
logger.info('test deeplist ... %s' % t)
assert t == [{'d1': {'d1k1': 'v1', 'd1k2': 'v2', 'd1ext': 'vext'}}, {'d2': {'d2k2': 'x2', 'd2k1': 'x1'}}, {'d32': {'a': 'A2A2', 'c': 'CCC', 'b': 'B2'}, 'd31': {'a': 'AAA', 'c': 'C', 'b': 'B'}}, {'dext1': {'d1k1ext': 'v1ext'}}]

t = conf.get('deepmap')
logger.info('test deepmap ... %s' % t)
assert t == {'l1k1' : {'l2k1': 'overwr', 'l2k2': 'abc', 'l2k3': 'new val'}, 'l1k2': {'l2k1': 'bli', 'l2k2': 'bla', 'l2k3': 'blub'}, 'l1k1ext': {'l2k1ext': 'ext'}}

t = conf['ext']
logger.info('test extonly ... %s' % t)
assert t == 'extendet only'

t = conf['missing_key']
logger.info('test missing_key ... %s' % t)
assert t == 'one'

t = conf['missing_key_parent']
logger.info('test missing_key_parent ... %s' % t)
assert t == {'a': 'b'}

t = conf['common_key']
logger.info('test common_key ... %s' % t)
assert t == {'common_subkey_deep': 'oneext', 'missing_key_base': 'val2', 'missing_key_ext': 'val2missingInBase'}

logger.info('test simple vals ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'base.yaml'),
        os.path.join(basepath, 'baseext.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )

t = conf['singel']
logger.info('test single val ... %s' % t)
assert t == 'ext'

t = conf['int']
logger.info('test int val ... %s' % t)
assert t == 10

t = conf['array']
logger.info('test list val ... %s' % t)
assert t == ['baseext1', 'baseext2']

t = conf['hash']
logger.info('test simple dict ... %s' % t)
assert t == {'ek1': 'be1', 'ek2': 'be2'}

t = conf['deeplist']
logger.info('test deeplist ... %s' % t)
assert t == [{'d1': {'d1ext': 'vext'}}, {'dext1': {'d1k1ext': 'v1ext'}}, {'d32': {'a': 'A2A2', 'c': 'CCC'}, 'd31': {'a': 'AAA'}}]

t = conf['deepmap']
logger.info('test deepmap ... %s' % t)
assert t == {'l1k1': {'l2k1': 'overwr', 'l2k3': 'new val'}, 'l1k1ext': {'l2k1ext': 'ext'}}

t = conf['ext']
logger.info('test extonly ... %s' % t)
assert t == 'extendet only'

try:
    conf['nosuchelement']
    raise Error
except KeyError as e:
    assert '%s' % e == '\'nosuchelement\''

logger.info('test merged vals ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'base.yaml'),
        os.path.join(basepath, 'baseext.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
        )

t = conf['singel']
logger.info('test single val ... %s' % t)
assert t == 'ext'

t = conf['int']
logger.info('test int val ... %s' % t)
assert t == 10

t = conf['array']
logger.info('test list val ... %s' % t)
assert t == ['base1', 'base2', 'baseext1', 'baseext2']

t = conf['hash']
logger.info('test simple dict ... %s' % t)
assert t == {'k1': 'b1', 'k2': 'b2', 'ek1': 'be1', 'ek2': 'be2'}

t = conf['deeplist']
logger.info('test deeplist ... %s' % t)
assert t == [{'d1': {'d1k1': 'v1', 'd1k2': 'v2', 'd1ext': 'vext'}}, {'d2': {'d2k2': 'x2', 'd2k1': 'x1'}}, {'d32': {'a': 'A2A2', 'c': 'CCC', 'b': 'B2'}, 'd31': {'a': 'AAA', 'c': 'C', 'b': 'B'}}, {'dext1': {'d1k1ext': 'v1ext'}}]

t = conf.get('deepmap')
logger.info('test deepmap ... %s' % t)
assert t == {'l1k1' : {'l2k1': 'overwr', 'l2k2': 'abc', 'l2k3': 'new val'}, 'l1k2': {'l2k1': 'bli', 'l2k2': 'bla', 'l2k3': 'blub'}, 'l1k1ext': {'l2k1ext': 'ext'}}

t = conf['ext']
logger.info('test extonly ... %s' % t)
assert t == 'extendet only'

t = conf['missing_key']
logger.info('test missing_key ... %s' % t)
assert t == 'one'

t = conf['missing_key_parent']
logger.info('test missing_key_parent ... %s' % t)
assert t == {'a': 'b'}

t = conf['common_key']
logger.info('test common_key ... %s' % t)
assert t == {'common_subkey_deep': 'oneext', 'missing_key_base': 'val2', 'missing_key_ext': 'val2missingInBase'}

try:
    conf['nosuchelement']
    raise Error
except KeyError as e:
    assert '%s' % e == '\'nosuchelement\''

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu
