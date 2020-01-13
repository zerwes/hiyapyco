#! /usr/bin/env python
# vim: set fileencoding=utf-8
from __future__ import unicode_literals
import sys
import os
import logging
import platform
import hiyapyco

from jinja2 import Environment, Undefined, DebugUndefined, StrictUndefined, UndefinedError

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
        os.path.join(basepath, 'interpolateunicode.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True
        )


t = conf['one']
logger.info('test unicode val ... %s' % t)
assert t == 'Öns'

t = conf['oneKorean']
logger.info('test unicode val ... %s' % t)
assert t == '하나'

t = conf['Zwö']
logger.info('test unicode key ... %s' % t)
assert t == 'ölybaba Öns zwö ... 40'

t = conf['UnicoDict']
logger.info('test unicode dict ... %s' % t)
assert t == { 'Umlkäy': 'Umlwäl', 'umlinterploate': 'UnIcöDe Umlwäl'}

t = conf['Röm']
logger.info('test Röm: \'%s\'' % t)
assert t == 'pîine prăjită şi ţuică'

t = conf['kor']
logger.info('test kor: \'%s\'' % t)
assert t == '韓國語똥'

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

