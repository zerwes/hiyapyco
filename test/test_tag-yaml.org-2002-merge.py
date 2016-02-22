#! /usr/bin/env python

import sys
import os
import logging
import platform
import hiyapyco
import pprint


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

logger.info('test tag:yaml.org,2002:merge with default yaml loader ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'tag-yaml.org-2002-merge.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        usedefaultyamlloader=True)

pprint.PrettyPrinter(indent=4).pprint(conf)

logger.info('test tag:yaml.org,2002:merge with odilody yaml loader ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'tag-yaml.org-2002-merge.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        usedefaultyamlloader=False)

pprint.PrettyPrinter(indent=4).pprint(conf)

"""
t = conf['singel']
logger.info('test single val ... %s' % t)
assert t == 'ext'
"""


print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

