# -*- coding: utf-8 -*-

from distutils.core import setup

import os
import usedup


def _load(filename):
    """Loads file contents from package base path."""
    base = os.path.dirname(os.path.abspath(__file__))
    loadfile = os.path.join(base, filename)
    with open(loadfile, 'r') as f_in:
        return f_in.read()


readme = _load('README.txt')
requires = [i for i in _load('requirements.txt').split('\n') if i.strip()]


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Utilities'
    ]


setup(name=usedup.__title__,
      version=usedup.__version__,
      description='Basic Datamine Admin Tools',
      long_description=readme,
      author=usedup.__author__,
      url='https://github.com/LeviKanwischer/usedup',
      packages=['usedup'],
      install_requires=requires,
      entry_points={'console_scripts': ['usedup = usedup.__main__:cli']},
      classifiers=classifiers
      )
