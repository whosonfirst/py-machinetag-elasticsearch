#!/usr/bin/env python

import os, sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/machinetag.elasticsearch.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
version = open("VERSION").read()
desc = open("README.md").read()

setup(
    name='machinetag.elasticsearch',
    namespace_packages=['machinetag', 'machinetag.elasticsearch', 'machinetag.elasticsearch.wildcard', 'machinetag.elasticsearch.hierarchy'],
    version=version,
    description='Python libraries for working with machinetags in Elasticsearch',
    author='Mapzen',
    url='https://github.com/whosonfirst/py-machinetag-elasticsearch',
    install_requires=[
        'machinetag>=1.4'
        ],
    dependency_links=[
        'https://github.com/whosonfirst/py-machinetag/tarball/master#egg=machinetag-1.4',
        ],
    packages=packages,
    scripts=[
        ],
    download_url='https://github.com/whosonfirst/py-machinetag-elasticsearch/releases/tag/' + version,
    license='BSD')
