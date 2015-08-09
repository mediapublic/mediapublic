"""A sample test module."""

# For pathname munging
import os

# The module that build_tests comes from.
from gabbi import driver

# We need access to the WSGI application that hosts our service
import functools
from pyramid.paster import get_app

# This is weird, and I'm sorry, but you need to curry in the INI file to
# configure the service
load_app = functools.partial(
    get_app,
    os.path.join(os.path.dirname(__file__), '..', '..', 'development.ini'),
    name='main'
)

# By convention the YAML files are put in a directory named
# "gabbits" that is in the same directory as the Python test file.
TESTS_DIR = 'gabbits'


def load_tests(loader, tests, pattern):
    """Provide a TestSuite to the discovery process."""
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    return driver.build_tests(test_dir, loader,
                              intercept=load_app,
                              )
