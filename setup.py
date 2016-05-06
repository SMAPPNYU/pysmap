import sys
from setuptools import setup

setup(name='pysmap',
	packages=['pysmap', 'pysmap.twitterutil', 'pysmap.ntwrk'],
	version='0.0.2',
	description='pysmapp is a set of tools for working with twitter data',
	author='yvan',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/pysmapp',
	keywords='twitter data tools pysmapp',
	license='MIT',
	install_requires=[
	  'smappdragon>=0.0.21'
	]
)