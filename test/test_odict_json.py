#! /usr/bin/env python

import sys
import os
import logging
import platform
import pprint

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(sys.argv[0])))))
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


logger.info('test conversion yaml 2 json ...')
confy = hiyapyco.load(
            os.path.join(basepath, 'odict.yaml'),
            method=hiyapyco.METHOD_SIMPLE,
            failonmissingfiles=True,
            interpolate=False
        )
confj = hiyapyco.load(
            hiyapyco.dumpjson(confy, indent=2),
            method=hiyapyco.METHOD_SIMPLE,
            failonmissingfiles=True,
            interpolate=False,
            json=True
        )
logger.info('test yaml and json conf are equal ...')
assert confy == confj

logger.info('compare yaml / json odict interploation using ODYLDo ...')
conf = hiyapyco.load(
            os.path.join(basepath, 'odict.yaml'),
            method=hiyapyco.METHOD_SIMPLE,
            failonmissingfiles=True,
            interpolate=True
        )
confj = hiyapyco.load(
            hiyapyco.dumpjson(confy, indent=2),
            method=hiyapyco.METHOD_SIMPLE,
            failonmissingfiles=True,
            interpolate=True,
            json=True
        )
#pprint.PrettyPrinter(indent=4).pprint(conf)
#pprint.PrettyPrinter(indent=4).pprint(confj)
assert conf == confj



logger.info('compare yaml / json odict interploation using default yaml and StrictUndefined ...')
hiyapyco.jinja2env = Environment(undefined=StrictUndefined)
# this should NOT raise a UndefinedError, but interpolation will fail!
conf = hiyapyco.load(
            os.path.join(basepath, 'odict.yaml'),
            method=hiyapyco.METHOD_SIMPLE,
            failonmissingfiles=True,
            interpolate=True,
            usedefaultyamlloader=True
        )
confj = hiyapyco.load(
            hiyapyco.dumpjson(confy, indent=2),
            method=hiyapyco.METHOD_SIMPLE,
            failonmissingfiles=True,
            interpolate=True,
            usedefaultyamlloader=True,
            json=True
        )
assert conf == confj


print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

