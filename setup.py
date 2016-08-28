from distutils.core import setup
from setuptools import find_packages

SRC_DIR = '.'

setup(
    name='tensorflow-diff-eq',
    version='0.1dev',
    package_dir={'tensorflow_diff_eq': SRC_DIR},
    packages=['tensorflow_diff_eq'],
    license='All rights reserved.',
    long_description=open('README.md').read(),
)