#! /usr/bin/env python

import sys
import os
import logging
import platform
try:
    from ruamel_yaml import YAML
except ModuleNotFoundError:
    from ruamel.yaml import YAML

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

logger.info("test ruamel yaml loader ...")


def ruamel_loader(stream):
    yaml = YAML(typ='safe')
    return yaml.load_all(stream)


conf = hiyapyco.load(os.path.join(basepath, "base.yaml"), loader_callback=ruamel_loader)

expected = {'singel': 'base', 'int': 1, 'array': ['base1', 'base2'], 'hash': {'k1': 'b1', 'k2': 'b2'}, 'deeplist': [{'d1': {'d1k1': 'v1', 'd1k2': 'v2'}}, {'d2': {'d2k1': 'x1', 'd2k2': 'x2'}}, {'d31': {'a': 'A', 'b': 'B', 'c': 'C'}, 'd32': {'a': 'A2', 'b': 'B2'}}], 'deepmap': {'l1k1': {'l2k1': 'xyz', 'l2k2': 'abc'}, 'l1k2': {'l2k1': 'bli', 'l2k2': 'bla', 'l2k3': 'blub'}}, 'missing_key': 'one', 'common_key': {'common_subkey_deep': 'one', 'missing_key_base': 'val2'}}

assert conf == expected

print("passed test %s" % __file__)
