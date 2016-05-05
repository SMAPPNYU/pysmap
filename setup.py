import sys
from setuptools import setup

setup(name='smappy',
	packages=['smappy', 'smappy.chirpy', 'smappy.ntwrk'],
	version='0.0.1',
	description='smappy is a set of tools for working with twitter data',
	author='yvan',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/smappy',
	keywords='twitter data tools smappy',
	license='MIT',
	install_requires=[
	  'smappdragon>=0.0.21'
	]
)