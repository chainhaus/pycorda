from setuptools import setup

setup(
	name='pycorda',
	version='0.31',
	author='Jamiel Sheikh',
	packages=['pycorda'],
	install_requires=[
		'jaydebeapi',
		'pandas',
		'matplotlib',
		'datetime',
		'requests'
	],
	include_package_data=True,
)