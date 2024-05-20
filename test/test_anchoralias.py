#! /usr/bin/env python

import sys
import os
import logging
import platform
import hiyapyco
import yaml

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

logger.info('test anchoralias merge ...')
conf = hiyapyco.load(
        os.path.join(basepath, 'anchoralias.yaml'),
        os.path.join(basepath, 'anchoralias2.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True,
        usedefaultyamlloader=True
        )

#print(hiyapyco.dump(conf))

t = conf['testvar']['simple']
logger.info('test simple ... %s' % t)
assert t == 'new text'

#print(conf['testvar']['list'])
t = conf['testvar']['list']
logger.info('test list ... %s' % t)
assert t == [{'alist1key': 'another value for alistkey1'}, {'alist2key': 'alist2val'}, {'alist3key': 'alist3val'}]

#print(conf['testvar']['listwithmerge'])
t = conf['testvar']['listwithmerge']
logger.info('test listwithmerge ... %s' % t)
assert t == {'alist1key': 'alist1val now updated', 'alist3key': 'alist3val', 'alist2key': 'alist2val'}

#print(conf['testvar']['dict'])
t = conf['testvar']['dict']
logger.info('test dict ... %s' % t)
assert t == {'adkey1': 'aaa1aa', 'adkey2': 'ad value 2', 'adkey3': 'xxx'}

#print(conf['testvar']['dictwithmerge'])
t = conf['testvar']['dictwithmerge']
logger.info('test dictwithmerge ... %s' % t)
assert t == {'adkey1': 'ad value 1', 'adkey2': 'bb2bb', 'adkey3': 'yyy'}

print('passed test %s' % __file__)
