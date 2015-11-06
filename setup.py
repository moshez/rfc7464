# Copyright (c) AUTHORS
# See LICENSE for details.

import setuptools
import versioneer

url = 'https://github.com/moshez/rfc7464'

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    url=url,
    name=url.split('/')[-1],
    author='Moshe Zadka',
    description='Implementation of RFC7464 codec',
    long_description=long_description,
    author_email='zadka.moshe@gmail.com',
    packages=setuptools.find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(), 
    license='MIT',
    copyright='2015',
)
