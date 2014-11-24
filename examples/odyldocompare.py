#! /usr/bin/env python
"""
PYTHONPATH=. python examples/odyldocompare.py [FILE]
"""
import hiyapyco.odyldo as odyldo
import yaml
import sys
import os



FILES = sys.argv[1:]
if not FILES:
	FILES = ['test/odyl.yaml']

for F in FILES:
	print ('='*60)

	print ('-'*10, ' ORIGINAL %s ' % F, '-'*10)
	f = open(F, 'r')
	ydata = yaml.safe_load(f)
	print(ydata)
	print ('-'*60)
	print (yaml.safe_dump(ydata, default_flow_style = False))

	print ('='*60)

	print ('-'*10, ' ODYLDo %s ' % F, '-'*10)
	f = open(F, 'r')
	ydata = odyldo.safe_load(f)
	print(ydata)
	print ('-'*60)
	print(odyldo.safe_dump(ydata, default_flow_style = False))
	print ('='*60)

