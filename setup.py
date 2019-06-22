from setuptools import setup

setup(
	name='pycorda',
	version='0.1',
	author='Jamiel Sheikh',
	packages=['pycorda'],
	install_requires=[
		'jaydebeapi',
		'pandas'
	],
	include_package_data=True,
)