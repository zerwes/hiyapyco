#! /usr/bin/env python

import sys
import os
import logging
import platform

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.realpath(os.path.abspath(sys.argv[0]))), "lib"
    ),
)
import testsetup

logger = testsetup.setup(sys.argv[1:])

basepath = os.path.dirname(os.path.realpath(__file__))

print(
    "start test %s for hiyapyco %s using python %s (loglevel:%s)"
    % (
        __file__,
        hiyapyco.__version__,
        platform.python_version(),
        logging.getLevelName(logger.getEffectiveLevel()),
    )
)

logger.info("test custom yaml loader ...")


def custom_loader(stream):
    """Mock loader that doesn't actually read the yaml file"""
    return [{"custom_yaml": 42}]


conf = hiyapyco.load(os.path.join(basepath, "base.yaml"), loader_callback=custom_loader)
assert conf == {"custom_yaml": 42}

print("passed test %s" % __file__)
