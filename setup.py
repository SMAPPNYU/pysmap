import sys
from setuptools import setup

setup(name='pysmap',
	packages=['pysmap', 'pysmap.twitterutil', 'pysmap.ntwrk', 'pysmap.viz'],
	version='0.0.8',
	description='pysmap is a set of tools for working with twitter data',
	author='yvan',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/pysmapp',
	keywords='twitter data tools pysmap',
	license='MIT',
	install_requires=[
	  'smappdragon>=0.0.21',
	  'stop-words>=2015.2.23.1'
	]
)