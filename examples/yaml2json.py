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
parser.add_argument(
        '-y', '--usedefaultyamlloader', dest='usedefaultyamlloader',
        action='store_true', default=False, help='use default yaml loader (default: False)'
    )
parser.add_argument(
        '-i', '--interpolate', dest='interpolate',
        action='store_true', default=False, help='use interpolation using jinja2 (default: False)'
    )
parser.add_argument('-f', '--file', type=str, nargs='+', help='yaml file(s) to parse')
parser.add_argument(
        '-j', '--json',
        type=str,
        action='store',
        dest='jsonfile',
        default=None,
        help='write json data to file (default: print dump)'
        )
args = parser.parse_args()

if args.loglevel is None:
    logging.disable(logging.CRITICAL)

# FIXME: in fact this should be the job of argparse
if args.file is None or len(args.file) == 0:
    raise Exception('please provide at least one yaml file!')

conf = hiyapyco.load(
    *args.file,
    usedefaultyamlloader=args.usedefaultyamlloader,
    interpolate=args.interpolate,
    failonmissingfiles=True
    )
if args.jsonfile is None:
    print('-'*10, 'YAML', '-'*10)
    print(hiyapyco.dump(conf))
    print('-'*10, 'JSON', '-'*10)
    print(hiyapyco.dumpjson(conf, indent=2))
else:
    jfp = open(args.jsonfile, 'w')
    hiyapyco.savejson(conf, jfp, indent=2)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

