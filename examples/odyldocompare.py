import odyldo
import yaml
import sys
import os




print '='*60

print '-'*10, ' ORIGINAL ', '-'*10
f = open('test/odyl.yaml', 'r')
ydata = yaml.safe_load(f)
print(ydata)
print '-'*60
print (yaml.safe_dump(ydata, default_flow_style = False))

print '='*60

print '-'*10, ' ODYLDo ', '-'*10
f = open('test/odyl.yaml', 'r')
ydata = odyldo.safe_load(f)
print(ydata)
print '-'*60
print(odyldo.safe_dump(ydata, default_flow_style = False))
print '='*60

