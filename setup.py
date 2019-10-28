# -*- coding: utf-8 -*-
#
#

"""
EasyLeague Setup File

This file will setup EasyLeague

Author: John Hsu and Sergey Satskiy

"""

import sys
import os.path
import platform
from setuptools import setup, Extension

description = 'This program will allow users to setup and run a table tennis league'


try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst').splitlines()

except Exception as exc:
    print('pypandoc package is not installed: the markdown '
          'README.md convertion to rst failed: ' + str(exc), file=sys.stderr)
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding='utf-8') as f:
        long_description = f.read()


# install_requires=['pypandoc'] could be added but really it needs to only
# at the time of submitting a package to Pypi so it is excluded from the
# dependencies
setup(name='easyleague',
      description=description,
      long_description=long_description,
      version="1.0.0",
      author='John Hsu',
      author_email='john1hsu@icloud.com',
      url='https://github.com/fivestarhobbes/EasyLeague',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3'],
      platforms=['any'],
      )
