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



logger.info('test missing file w/ default value for failonmissingfiles ...')
try:
    conf = hiyapyco.HiYaPyCo(
        os.path.join(basepath, 'base.yaml'),
        'nosuchfile.yaml'
        )
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert '%s' % e == 'yaml file not found: \'nosuchfile.yaml\''

logger.info('test missing file as list w/ default value for failonmissingfiles ...')
try:
    conf = hiyapyco.HiYaPyCo([
        os.path.join(basepath, 'base.yaml'),
        'nosuchfile.yaml',
        ])
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert '%s' % e == 'yaml file not found: \'nosuchfile.yaml\''

logger.info('test missing file w/ failonmissingfiles=False ...')
conf = hiyapyco.HiYaPyCo(
    os.path.join(basepath, 'm.yaml'),
    'nosuchfile.yaml',
    os.path.join(basepath, 'm1.yaml'),
    os.path.join(basepath, 'm2.yaml'),
    os.path.join(basepath, 'm3.yaml'),
    failonmissingfiles=False
    )
assert conf.yamlfiles() == [
        os.path.join(basepath, 'm.yaml'),
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        ]
assert '%s' % conf == 'hiyapyco [%s]' % os.pathsep.join([
        os.path.join(basepath, 'm.yaml'),
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        ])
assert conf.data() == {'m': ['a', 'b', 'c'], 'm1': 'abc', 'm2': 'xyz', 'm3': 123}

logger.info('test missing file as list w/ failonmissingfiles=False ...')
conf = hiyapyco.HiYaPyCo(
    [
        os.path.join(basepath, 'm.yaml'),
        'nosuchfile.yaml',
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
    ],
    failonmissingfiles=False
    )
assert conf.yamlfiles() == [
        os.path.join(basepath, 'm.yaml'),
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        ]
assert '%s' % conf == 'hiyapyco [%s]' % os.pathsep.join([
        os.path.join(basepath, 'm.yaml'),
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        ])
assert conf.data() == {'m': ['a', 'b', 'c'], 'm1': 'abc', 'm2': 'xyz', 'm3': 123}

logger.info('test deep merge w/ missing file as list w/ failonmissingfiles=False ...')
conf = hiyapyco.HiYaPyCo(
    [
        os.path.join(basepath, 'm.yaml'),
        'nosuchfile.yaml',
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        os.path.join(basepath, 'm4.yaml'),
    ],
    failonmissingfiles=False,
    method=hiyapyco.METHOD_MERGE
    )
assert conf.yamlfiles() == [
        os.path.join(basepath, 'm.yaml'),
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        os.path.join(basepath, 'm4.yaml'),
        ]
assert '%s' % conf == 'hiyapyco [%s]' % os.pathsep.join([
        os.path.join(basepath, 'm.yaml'),
        os.path.join(basepath, 'm1.yaml'),
        os.path.join(basepath, 'm2.yaml'),
        os.path.join(basepath, 'm3.yaml'),
        os.path.join(basepath, 'm4.yaml'),
        ])
assert conf.data() == {'m': ['a', 'b', 'c', 'd', 'e', 'f'], 'm1': 'abc', 'm2': 'xyz', 'm3': 123}

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

