#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='nppm',
    version='0.1.2',
    description='An npm-like tool for Python projects',
    url='https://github.com/emallson/nppm',
    author='J David Smith',
    author_email='emallson@atlanis.net',
    license='GPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        'Programming Language :: Python :: 3'
    ],
    keywords='development',
    packages=find_packages(),
    install_requires=['pip', 'ipython', 'semver'],
    entry_points={
        'console_scripts': [
            'nppm=nppm.main:main',
            'ppm=nppm.main:main'
        ],
    },
)
