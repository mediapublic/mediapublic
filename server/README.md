mediapublic README
==================

Requirements
------------

The mediapublic pyramid server is built for Python 3.3 and above. It provides
the REST API and storage to the JS frontend application.

Pre-Getting Started

- Install virtualenv and virtualenv-wrapper ( http://docs.python-guide.org/en/latest/dev/virtualenvs/ )

- Create virtual env with python3 ( `mkvirtualenv --python $(which python3) mediapublic` )

Getting Started
---------------

- cd <directory containing this file>

- Activate your virtualenv ( `workon mediapublic` )

- `pip install -e . # this installs mediapublic and its dependencies`

- `initialize_mediapublic_db development.ini`

- `pserve development.ini --reload`

Running Tests
-------------

Currently, the only tests are API tests (using [gabbi][gabbi]) and PEP8 checks.
These can be run using [tox][tox] (`pip install tox`).

```
# run all tests
tox

# run just the API tests
tox -egabbi

# run just the PEP8 checks
tox -epep8
```

[gabbi]: http://gabbi.readthedocs.org/
[tox]: http://tox.testrun.org/
