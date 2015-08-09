mediapublic README
==================

Requirements
------------

The mediapublic pyramid server is built for Python 3.3 and above. It provides
the REST API and storage to the JS frontend application.

Getting Started
---------------

- cd <directory containing this file>

- Activate an appropriate virtualenv

- `pip install -e . # this installs mediapublic and its dependencies`

- `initialize_mediapublic_db development.ini`

- `pserve development.ini`

Running Tests
-------------

Currently, the only tests are API tests (using [gabbi][gabbi]) and PEP8 checks.
These can be run using [tox][tox].

```
# API tests
tox -egabbi

# PEP8 checks
tox -epep8
```

[gabbi]: http://gabbi.readthedocs.org/
[tox]: http://tox.testrun.org/
