from setuptools import find_packages, setup

setup(
	name='escratsou',
	packages=find_packages(include=['escratsou']),
	version='25.7.25',
	description='Helps with datapack creation for Minecraft',
	author='artitapheiont',
	license='MIT',
	install_requires=[],
	setup_requires=['pytest-runner'],
	tests_require=['pytest'],
	test_suite='tests'
)