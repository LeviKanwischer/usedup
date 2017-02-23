::

                                           _/
      _/    _/    _/_/_/    _/_/      _/_/_/  _/    _/  _/_/_/
     _/    _/  _/_/      _/_/_/_/  _/    _/  _/    _/  _/    _/
    _/    _/      _/_/  _/        _/    _/  _/    _/  _/    _/
     _/_/_/  _/_/_/      _/_/_/    _/_/_/    _/_/_/  _/_/_/
                                                    _/
                                                   _/


*Datamine (Upsight.com) CLI Admin Tool*


OVERVIEW
''''''''
usedup is a simple command line tool for performing basic admin tasks using both official and unofficial DataMine api's. At present this allows for; checking currently running queries, viewing a running queries stats, killing active queries, and/or downloading an archive of historicly run queries. Since login is required to access DataMine(Upsight.com), user credentials will be asked upon submitting each command. A config file can be configured at ~/usedup with `username` and `password` declared under a `usedup` section. If this is present, credentials will not be required.


USAGE
'''''
.. code-block::

    Usage: usedup [OPTIONS] COMMAND [ARGS]...

        Datamine (Upsight.com) CLI Admin Tool

        usedup is a simple command line tool for performing basic admin tasks
        using both official and unofficial DataMine api's. At present this allows
        for; checking currently running queries, viewing a running queries stats,
        killing active queries, and/or downloading an archive of historicly run
        queries. Since login is required to access DataMine(Upsight.com), user
        credentials will be asked upon submitting each command.

        USAGE:
            $ usedup --help

        See the README for further details.

    Options:
        --help  Show this message and exit.

    Commands:
        history  Download an archive of previously run queries.
        kill     Kill actively running query using Upsight's Query ID.
        running  Print list of currently running queries.
        status   Print details about active query Upsight's Query ID.


INSTALL
'''''''
.. code-block:: bash

    $ python -m pip install git+https://github.com/levikanwischer/usedup.git


TESTING
'''''''
This package has been test free since 83'.
