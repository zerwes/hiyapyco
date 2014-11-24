#! /usr/bin/env python

import sys
import os
import logging
import argparse

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import hiyapyco

class LoggingAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print '%r %r %r' % (namespace, values, option_string)
        logger = logging.getLogger()
        logger.setLevel(values)
        setattr(namespace, self.dest, values)

logger = logging.getLogger()
logging.basicConfig(
    level=logging.WARN,
    format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
    )

parser = argparse.ArgumentParser()
parser.add_argument(
    '-l', '--loglevel',
    help='set loglevel',
    type=str,
    choices=[k for k in logging._levelNames.keys() if isinstance(k, str)],
    action=LoggingAction
    )
parser.add_argument('-f', '--file', type=str, nargs='+', help='yaml file(s) to parse')
args = parser.parse_args()

if args.loglevel is None:
    logging.disable(logging.CRITICAL)

# FIXME: in fact this should be the job of argparse
if args.file is None or len(args.file) == 0:
    raise Exception('please provide at least one yaml file!')

for mergemethod in hiyapyco.METHODS.keys():
    print('='*10, 'method=', mergemethod, '='*10)
    conf = hiyapyco.load(
        *args.file,
        method=hiyapyco.METHODS[mergemethod],
        interpolate=True,
        failonmissingfiles=True
        )
    print(conf)
    print('-'*10, 'YAML', '-'*10)
    print(hiyapyco.dump(conf))
    if len(args.file) < 2:
        break

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

