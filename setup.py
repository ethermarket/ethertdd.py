#!/usr/bin/env python

from distutils.core import setup

setup(name='EtherTDD.py',
      version='0.1.2',
      description='Ethereum unit testing tool.',
      author='Ryan Casey',
      author_email='ryan@ryepdx.com',
      url='https://github.com/ryepdx/ethertdd.py/',
      packages=['ethertdd'],
      requires=['pyethereum']
)
