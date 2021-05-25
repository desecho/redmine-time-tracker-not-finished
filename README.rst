Redmine-time-tracker
==========================================================

Details:
---------
Import project view imports projects on which a user has worked during `PROJECT_IMPORT_NUMBER_OF_MONTHS` number of months.


Development
----------------

.. code:: bash
    pip install -r requirements.txt

Use `clean.sh` to automatically "isort" your code.

Use `tox` for testing and linting.

Installation
----------------

.. code:: bash

    mkvirtualenv -p /usr/bin/python3.4 redmine_tracker
    bower install
    pip install -r requirements.txt
