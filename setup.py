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
    long_description = pypandoc.convert_file('README.md', 'rst')

except Exception as exc:
    print('pypandoc package is not installed: the markdown '
          'README.md convertion to rst failed: ' + str(exc), file=sys.stderr)
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding='utf-8') as f:
        long_description = f.read()


def getPackageData():
    """Provides the data files"""
    extensions = ['.png']
    package_data = [('img',
                     'img/')]

    # If a skin needs to be added, then the following item should be also
    # appended:
    # package_data.append(('codimension.skins.myskin',
    #                      'codimension/skins/myskin/'))

    result = {}
    for item in package_data:
        package = item[0]
        matchFiles = []
        for fName in os.listdir(item[1]):
            for ext in extensions:
                if fName.endswith(ext):
                    matchFiles.append(fName)
                    break
        if matchFiles:
            result[package] = matchFiles
    return result


# install_requires=['pypandoc'] could be added but really it needs to only
# at the time of submitting a package to Pypi so it is excluded from the
# dependencies
setup(name='easyleague',
      description=description,
      python_requires='>=3.7',
      long_description=long_description,
      version="1.0.2",
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
      packages=['src'],
      package_data=getPackageData(),
      install_requires=['PyQt5==5.13.2'],
      entry_points={'gui_scripts': ['easyleague = src.easyleague:main']}
      )
