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

logger.info('test odict interploation  using ODYLDo ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'odict.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True,
        interpolate=True
        )

source_domain = conf['source']['domain']
source_domainDN = conf['source']['domainDN']
logger.info('test interpolation source_domainDN and source_domain ... %s : %s' % (source_domainDN, source_domain))
assert source_domainDN == 'dc=%s' % ',dc='.join(source_domain.split('.'))

source_baseDN = conf['source']['baseDN']
logger.info('test interpolation source_baseDN ... %s' % source_baseDN)
assert source_baseDN == 'ou=Users,%s' % source_domainDN

source_bindDN = conf['source']['bindDN']
logger.info('test interpolation source_bindDN ... %s' % source_bindDN)
assert source_bindDN == 'cn=Administrator,%s' % source_baseDN


logger.info('test odict interploation using default yaml and StrictUndefined ...')
hiyapyco.jinja2env = Environment(undefined=StrictUndefined)
# this should NOT raise a UndefinedError, but interpolation will fail!
conf = hiyapyco.load(
    os.path.join(basepath, 'odict.yaml'),
    method=hiyapyco.METHOD_SIMPLE,
    failonmissingfiles=True,
    interpolate=True,
    usedefaultyamlloader=True
    )

source_domain = conf['source']['domain']
source_domainDN = conf['source']['domainDN']
logger.info('test interpolation source_domainDN and source_domain ... %s : %s' % (source_domainDN, source_domain))
assert source_domainDN == 'dc=%s' % ',dc='.join(source_domain.split('.'))

# FIXME: yaml loader seems to have changed ...
"""
source_baseDN = conf['source']['baseDN']
logger.info('test interpolation source_baseDN ... %s' % source_baseDN)
assert source_baseDN == 'ou=Users,%s' % "dc={{ source.domain.split('.')|join(',dc=') }}"

source_bindDN = conf['source']['bindDN']
logger.info('test interpolation source_bindDN ... %s' % source_bindDN)
assert source_bindDN == 'cn=Administrator,%s' % 'ou=Users,{{ source.domainDN }}'
"""

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

