# Copyright (c) Moshe Zadka
# See LICENSE for details.
import setuptools
import versioneer

url = 'https://github.com/moshez/rfc7464'
setuptools.setup(
    url=url,
    name=url.split('/')[-1],
    author='Moshe Zadka',
    author_email='zadka.moshe@gmail.com',
    packages=setuptools.find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(), 
)
