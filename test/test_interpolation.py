#! /usr/bin/env python

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
        os.path.join(basepath, 'interpolate.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True
        )
t1 = conf.get('first')
t2 = conf.get('firstcopy')
t3 = conf['second']
logger.info('test first interpolation ... %s : %s' % (t1, t2,))
assert t1 == t2
logger.info('test second interpolation ... %s : %s' % (t1, t3,))
assert t3 == 'again %s' % t1

t = conf.get('list')
logger.info('test interpolation in list ... %s' % t)
assert t == ['abc', 'bcd', 'cde', 'abc']

t = conf['elist']
logger.info('test elist ... %s' % t)
assert t is None

t = conf['deep']['interp']
logger.info('test deep interpolation ... %s' % t)
assert t == {'str': '10 + 23', 'sum': '33', 'join': 'ali baba and the 40 thieves'}

t = conf['m']
logger.info('test more interpolation ... %s' % t)
assert t == [{'a': 'A', 'b': '', 'c': 'ALI BABA'}, {'a': 'B', 'b': 'again first element', 'c': 'C & {{ m.0.a }}'}, {'a': 'C & A', 'b': 'cc', 'c': 'ccc'}]

logger.info('test StrictUndefined ...')
hiyapyco.jinja2env = Environment(undefined=StrictUndefined)
try:
    conf = hiyapyco.HiYaPyCo(
        os.path.join(basepath, 'interpolate.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True
        )
except hiyapyco.HiYaPyCoImplementationException as e:
    logger.info('test UndefinedError: "%s"' % e)
    undefmsg = '\'undefined\' is undefined'
    hiyapmsg = 'error interpolating string "{{ undefined }}"'
    assert '%s' % e == '%s : %s' % (hiyapmsg, undefmsg,) or '%s' % e == '%s : b"%s"' % (hiyapmsg, undefmsg,)


logger.info('test DebugUndefined ...')
hiyapyco.jinja2env = Environment(undefined=DebugUndefined)
conf = hiyapyco.load(
        os.path.join(basepath, 'interpolate.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True
        )
t = conf['m']
logger.info('test debugundefined interpolation ... %s' % t)
assert t == [{'a': 'A', 'b': '{{ undefined }}', 'c': 'ALI BABA'}, {'a': 'B', 'b': 'again first element', 'c': 'C & {{ m.0.a }}'}, {'a': 'C & A', 'b': 'cc', 'c': 'ccc'}]

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

