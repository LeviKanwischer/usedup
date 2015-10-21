                                       _/                     
  _/    _/    _/_/_/    _/_/      _/_/_/  _/    _/  _/_/_/    
 _/    _/  _/_/      _/_/_/_/  _/    _/  _/    _/  _/    _/   
_/    _/      _/_/  _/        _/    _/  _/    _/  _/    _/    
 _/_/_/  _/_/_/      _/_/_/    _/_/_/    _/_/_/  _/_/_/       
                                                _/            
                                               _/             
Basic Datamine Admin Tools


OVERVIEW:
usedup is a simple command line tool for performing basic admin tasks
using both official and unofficial datamine api's. At present this allows
for; checking currently running queries, viewing a running queries stats,
killing active queries, and/or downloading an archive of historicly run
queries. Since login is required to access datamine(upsight.com), user
credentials will be asked upon submitting each command.

To run, simply pip install (See: INSTALL), then run (See: USAGE) in the 
console of your choice. Current implementation has only 
been tested on Python 3.4+. Minimal exceptions have been handled for.


REQUIREMENTS:
- Python 3.4+
- requirements.txt


INSTALL:
$ python -m pip install git+https://github.com/LeviKanwischer/usedup


USAGE:
$ usedup --help


STRUCTURE:
usedup
├── README.txt
├── LICENSE.txt
├── requirements.txt
├── setup.py
└── usedup
    ├── __init__.py
    ├── __main__.py
    └── usedup.py


TODO:
- Test/Add Python 2.7+ compatibility
- Improve printing format of `details`
