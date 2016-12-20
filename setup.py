import sys
from setuptools import setup

setup(name='pysmap',
	packages=['pysmap', 'pysmap.twitterutil', 'pysmap.viz'],
	version='0.0.26',
	description='pysmap is a set of tools for working with twitter data',
	author='yvan',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/pysmapp',
	keywords='twitter data tools pysmap',
	license='MIT',
	install_requires=[
	  'smappdragon',
	  'stop-words>=2015.2.23.1',
	  'langdetect>=1.0.6',
	  'bokeh>=0.11.1',
	  'pandas>=0.18.1',
	  'pymongo>=3.2.2',
	  'pytz>=2016.4'
	]
)