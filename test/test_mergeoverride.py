#! /usr/bin/env python

import sys
import os
import logging
import platform
import hiyapyco
import semantic_version as semver

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

def semver_merge(a, b, context):
    if context[0] == 'bypass': return b
    if a is None or b is None: return b
    try:
        # We have to manually decompose these since lib doesn't appear to
        # have built in comparisons for one Spec against another (only Version)
        lhs = semver.SimpleSpec(a)
        rhs = semver.SimpleSpec(b)
        # TODO: Not always a Range clause
        lhs_target = lhs.clause.target
        rhs_target = rhs.clause.target
        if lhs_target > rhs_target:
            return a
        # DEBT: Crude
        elif (lhs.clause.operator == lhs.clause.OP_GT or
            lhs.clause.operator == lhs.clause.OP_GTE and
            rhs.clause.operator == rhs.clause.OP_EQ):
            return a
        return b
    except ValueError:
        return b

logger.info('test merge override vals ...')
h = hiyapyco.HiYaPyCo(
        os.path.join(basepath, 'mo1.yaml'),
        os.path.join(basepath, 'mo2.yaml'),
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True,
        mergeoverride=semver_merge
        )
conf = h.data()

assert h.mergeprimitive is not None

t = conf['depends']
t = t['lib1']
logger.info('test single val ... %s' % t)
#assert t == { 'lib1': '>=2.0.0' }
assert t == '>=2.0.0'

t = conf['depends']['lib2']
assert t == '2.0.0'

t = conf['bypass']['lib1']
assert t == '1.0.0'

try:
    conf['nosuchelement']
    raise Error
except KeyError as e:
    assert '%s' % e == '\'nosuchelement\''

print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu
