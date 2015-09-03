# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

import logging
import argparse

class LoggingAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # print '%r %r %r' % (namespace, values, option_string)
        logger = logging.getLogger()
        logger.setLevel(values)
        setattr(namespace, self.dest, values)

def setup_parser(args):
    try:
        # python 3.4 up ...
        loggingchoices = logging._nameToLevel.keys()
    except AttributeError:
        loggingchoices = [k for k in logging._levelNames.keys() if isinstance(k, str)]
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-l', '--loglevel',
            help='set loglevel',
            type=str,
            choices=loggingchoices,
            action=LoggingAction
            )
    return parser.parse_args(args)

def setup(args):
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.WARN,
        format='%(levelname)s\t[%(name)s] %(funcName)s: %(message)s'
        )
    args = setup_parser(args)
    if args.loglevel is None:
        logging.disable(logging.CRITICAL)
    return logger

