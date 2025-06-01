#! /usr/bin/env python

import sys
import os
import logging
import platform

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))
import hiyapyco

sys.path.insert(0, os.path.join(basepath, 'lib'))
import testsetup

logger = testsetup.setup(sys.argv[1:])

print('start test %s for hiyapyco %s using python %s (loglevel:%s)' % (
            __file__,
            hiyapyco.__version__,
            platform.python_version(),
            logging.getLevelName(logger.getEffectiveLevel())
        )
    )


logger.info("test none behavior IGNORE ...")
conf = hiyapyco.load(
    os.path.join(basepath, "base.yaml"),
    os.path.join(basepath, "base_none_behavior_empty_dict.yaml"),
    none_behavior=hiyapyco.NONE_BEHAVIOR_IGNORE,
    method=hiyapyco.METHOD_MERGE,
    failonmissingfiles=True,
)

t = conf["deepmap"]
logger.info("test deepmap ... %s" % t)
assert t == {
    "l1k1": {"l2k1": "abc", "l2k2": "abcabc"},
    "l1k2": {"l2k1": "bli", "l2k2": "bla", "l2k3": "blub"},
}

print("passed test %s" % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu
