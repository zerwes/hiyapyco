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

yamlfile = os.path.join(basepath, 'castinterpolated.yaml')

logger.info('test uncasted ...')
conf = hiyapyco.load(
        yamlfile,
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True,
        )
v = conf['three']
logger.info('test uncasted: %s (type: %s) ... ' % (v, type(v),))
assert v == '3'
v = conf['c']
logger.info('test uncasted: %s (type: %s) ... ' % (v, type(v),))
assert v == '5.9'
v = conf['bool']
logger.info('test uncasted: %s (type: %s) ... ' % (v, type(v),))
assert v == 'True'

conf = hiyapyco.load(
        yamlfile,
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True,
        castinterpolated=True,
        )
v = conf['three']
logger.info('test casted: %s (type: %s) ... ' % (v, type(v),))
assert v == 3
v = conf['c']
logger.info('test casted: %s (type: %s) ... ' % (v, type(v),))
assert v == 5.9
v = conf['bool']
logger.info('test casted: %s (type: %s) ... ' % (v, type(v),))
assert v == True

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

