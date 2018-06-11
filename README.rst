Tool for crawling and exporting data data from Untappd public site
==================================================================


Note
----

This is still early in the development and a bit rough around the edges.
Any bug reports, feature suggestions, etc are greatly appreciated. :)


Installation and usage
----------------------

**Installation**
Since this is a Python package available on PyPi you can install it like 
any other Python package.

.. code-block:: shell

    # on modern systems with Python you can install with pip
    $ pip install untappd_crawler
    # on older systems you can install using easy_install
    $ easy_install untappd_crawler

**Usage**
The commands should be mostly self-documenting in how they are defined,
which is made available through the ``help`` command.

.. code-block:: shell

    $ untappd_crawler
    usage: untappd_crawler -o <output_file_path> [-u <username>] [-b <beer_ids_repeated>]

    arguments:
      -h, --help            show this help message and exit
      Rest are in the help
