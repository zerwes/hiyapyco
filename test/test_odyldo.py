import odyldo
import yaml
import sys
import os

f = open('odyl.yaml', 'r')
ydata = yaml.load(f, odyldo.ODYL)

print ydata

print (yaml.safe_dump(ydata, default_flow_style = False))

