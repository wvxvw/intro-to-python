#!/usr/bin/env python

from setuptools import setup

setup(
    name='intro_to_python',
    version='1.0',
    description='Programming assignments from CS1101',
    author='Oleg Sivokon',
    author_email='olegsivokon@gmail.com',
    url='https://github.com/wvxvw/intro-to-python',
    packages=[
        'intro_to_python',
        'intro_to_python.assignment2'
    ],
    package_dir={'intro_to_python': 'intro_to_python'},
    package_data={'intro_to_python': ['etc/*.*']},
    scripts=['scripts/t_area'],
    install_requires=[
        'configparser >= 3.5.0',
    ],
)
