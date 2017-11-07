#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A setuptools based setup module for merkleshare"""

from codecs import open
from os import path
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from subprocess import call


import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open(path.join(here, 'requirements_test.txt'), encoding='utf-8') as reqs:
    test_requirements = reqs.read().split('\n')[:-1]


setup_requirements = [
    'pytest-runner',
]

install_requirements = [
    'base58',
    'cryptography',
    'ipfsapi',
    'jinja2',
    'morphys',
]

cmdclass_dict = versioneer.get_cmdclass()


# Versioneer already implements a custom build_py - we need to extend it
class NPMBuildPyCommand(cmdclass_dict['build_py']):
    def run(self):
        # Call versioneer's custom build_py
        super(NPMBuildPyCommand, self).run()

        # Install JS dependencies and generate the HTML template
        assert call(['npm', 'install']) == 0


cmdclass_dict['build_py'] = NPMBuildPyCommand

setup(
    name='merkleshare',
    version=versioneer.get_version(),
    cmdclass=cmdclass_dict,
    description="A no-brainer pastebin on IPFS - " +
    "think distributed http://sprunge.us",
    long_description=readme + '\n\n' + history,
    author="Stanislaw Drozd",
    author_email='drozdziak1@gmail.com',
    url='https://github.com/drozdziak1/merkleshare',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'mersh=merkleshare.merkleshare:main',
        ],
    },
    include_package_data=True,
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    license="MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    package_data={'': ['output/*.html']}
)
