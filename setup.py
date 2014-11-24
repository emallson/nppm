#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ppm',
    version='0.1.0',
    description='An NPM-like tool for Python',
    url='https://github.com/emallson/ppm',
    author='J David Smith',
    author_email='emallson@atlanis.net',
    license='GPL',
    classifiers=[
        'Developement Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3'
    ],
    keywords='development',
    packages=find_packages(),
    install_requires=['pip', 'ipython', 'semver'],
    entry_points={
        'console_scripts': [
            'ppm=ppm.main:main'
        ],
    },
)
