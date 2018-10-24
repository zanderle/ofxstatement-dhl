#!/usr/bin/python3
"""Setup
#Note: To publish new version: `./setup.py sdist upload`
"""
import os
from setuptools import find_packages
from distutils.core import setup

version = "1.0.0"

setup(name='ofxstatement-dhl',
      version=version,
      author="Žan Anderle",
      author_email="zan.anderle@gmail.com",
      url="https://github.com/zanderle/ofxstatement-dhl",
      description=("Bank statement parser for Delavska Hranilnica (Slovenija)"),
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      license="GPLv3",
      keywords=["ofx", "ofxstatement", "banking", "statement"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          'ofxstatement': [
              'dhl = ofxstatement.plugins.dhl:DHLPlugin',
          ]
      },
      install_requires=['ofxstatement'],
      include_package_data=True,
      zip_safe=True
      )
