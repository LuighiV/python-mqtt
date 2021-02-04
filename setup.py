#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup

from paho.mqtt import __version__

with open('README.md', 'rb') as readme_file:
    readme = readme_file.read().decode('utf-8')

requirements = []
setup_requirements = [] 

setup(
    name='paho-mqtt',
    version=__version__,
    description='MQTT client class adapted for Digi Device',
    long_description=readme,
    author='Digi Team',
    author_email='roger@atchoo.org',
    url='http://eclipse.org/paho',
    packages=['paho', 'paho.mqtt'],
    license='Mozilla Public License, v. 2.0.',
    keywords='paho',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6.1',
        'Topic :: Communications',
        'Topic :: Internet',
    ],
)
