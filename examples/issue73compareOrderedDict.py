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
    choices=[k for k in logging._nameToLevel.keys() if isinstance(k, str)],
    action=LoggingAction
    )
parser.add_argument('-f', '--file', type=str, nargs='+', required=True, help='yaml file(s) to parse')
args = parser.parse_args()

if args.loglevel is None:
    logging.disable(logging.INFO)

# FIXME: in fact this should be the job of argparse
if args.file is None or len(args.file) == 0:
    raise Exception('please provide at least one yaml file!')

for  usedefaultyamlloader in [True, False]:
    print('='*10, 'usedefaultyamlloader=', usedefaultyamlloader, '='*10)
    conf = hiyapyco.load(
        *args.file,
        method=hiyapyco.METHOD_MERGE,
        interpolate=True,
        failonmissingfiles=True,
        usedefaultyamlloader=usedefaultyamlloader
        )
    print(conf)
    print('-'*10, 'YAML', '-'*10)
    print(hiyapyco.dump(conf, default_flow_style=False))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

