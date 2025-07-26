from setuptools import find_packages, setup
import datetime
date = str(datetime.datetime.now().date()).split('-')

setup(
	name='escratsou',
	packages=find_packages(include=['escratsou']),
	version=str(int(date[2])) + '.' + str(int(date[1])) + '.' + str(int(date[0][2] + date[0][3])),
	description='Creates datapacks and resourcepacks for Minecraft',
	url='https://github.com/artelephantb/escratsou',
	author='artitapheiont',
	license='MIT',
	install_requires=[],
	package_data={ 'escratsou': ['datapack/*'] },
	setup_requires=['pytest-runner'],
	tests_require=['pytest'],
	test_suite='tests'
)
