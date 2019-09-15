from setuptools import setup

setup(
	name='pycorda',
	version='0.35',
	author='Jamiel Sheikh',
	packages=['pycorda'],
	install_requires=[
		'jaydebeapi',
		'pandas',
		'matplotlib',
		'datetime',
		'requests',
		'pyjks'

	],
	include_package_data=True,
)