from setuptools import setup, find_packages
setup(name=lmu-dataset, version=0.1.0, packages=find_packages(), install_requires=[
    requests, beautifulsoup4, html5lib, python-dateutil, urllib3
])
