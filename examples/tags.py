#! /usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

import sys
import os

basepath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(basepath))

import yaml
import hiyapyco

class GenericElement(yaml.YAMLObject):
    def __init__(self, value, tag, style=None):
        self._value = value
        self._tag = tag
        self._style = style

    def to_yaml(dumper, data):
        return dumper.represent_scalar(data._tag, data._value, style=data._style)

def unknown_tag_handler(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return GenericElement(node.value, tag_suffix, style=node.style)
    else:
        raise NotImplementedError('Node: ' + str(type(node)))

yaml.add_multi_constructor('', unknown_tag_handler, Loader=yaml.SafeLoader)
yaml.add_representer(GenericElement, GenericElement.to_yaml, Dumper=yaml.SafeDumper)

conf = hiyapyco.load(
    os.path.join(basepath, 'tags.yaml'),
    method=hiyapyco.METHOD_SIMPLE,
    usedefaultyamlloader=True,
    failonmissingfiles=True
    )
print(hiyapyco.dump(conf))
