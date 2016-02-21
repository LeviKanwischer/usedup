:: 

                                           _/                     
      _/    _/    _/_/_/    _/_/      _/_/_/  _/    _/  _/_/_/    
     _/    _/  _/_/      _/_/_/_/  _/    _/  _/    _/  _/    _/   
    _/    _/      _/_/  _/        _/    _/  _/    _/  _/    _/    
     _/_/_/  _/_/_/      _/_/_/    _/_/_/    _/_/_/  _/_/_/       
                                                    _/            
                                                   _/             


*Datamine (Upsight.com) CLI Admin Tools*


.. image:: https://img.shields.io/pypi/v/usedup.svg
    :target: https://pypi.python.org/pypi/usedup


OVERVIEW
''''''''
usedup is a simple command line tool for performing basic admin tasks.
At present this allows for; checking currently running queries, viewing
a running queries stats, killing active queries, and/or extracting user
run query archives. Since login is required to access Upsight.com, user
credentials are stored in plain test in a ~/.usedup.ini file.


USAGE
'''''
.. code-block:: bash

    Usage: usedup [OPTIONS] COMMAND [ARGS]...

    Options:
        --help  Show this message and exit.

    Commands:
        details  View active query details.
        history  Extract past user queries.
        kill     Cancel active query.
        running  Currently running queries.


INSTALL
'''''''
.. code-block:: bash

    $ python -m pip install usedup
