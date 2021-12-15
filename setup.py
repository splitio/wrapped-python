"""Setup module."""
# !/usr/bin/env python

from setuptools import setup, find_packages

TESTS_REQUIRES = [
    'flake8',
    'pytest>=6.2.3',
    'pytest-mock>=3.5.1',
    'coverage',
    'pytest-cov',
    'importlib-metadata==4.2'
]

setup(
    name="splitio_wrapper",
    version="0.0.1",
    packages=find_packages(),
    tests_require=TESTS_REQUIRES,
    extras_require={
        'test': TESTS_REQUIRES,
    },
    setup_requires=['pytest-runner'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)