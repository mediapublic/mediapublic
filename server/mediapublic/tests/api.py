"""A sample test module."""

# For pathname munging
import os
import functools

# The module that build_tests comes from.
from gabbi import driver

# pyramid configs
from pyramid.paster import get_app, get_appsettings
from sqlalchemy import engine_from_config

# models to start DB
from mediapublic.models import DBSession, Base

# This is weird, and I'm sorry, but you need to curry in the INI file to
# configure the service
config_path = os.path.join(os.path.dirname(__file__), 'gabbi.ini'),

try:
    # delete the old DB to start fresh
    os.remove(os.path.join(os.path.dirname(__file__), 'mediapublic.sqlite'))
except:
    # it may not exist, whatever
    pass

settings = get_appsettings(config_path)
engine = engine_from_config(settings, 'sqlalchemy.')
DBSession.configure(bind=engine)
Base.metadata.create_all(engine)


load_app = functools.partial(get_app, config_path, name='main')

# By convention the YAML files are put in a directory named
# "gabbits" that is in the same directory as the Python test file.
TESTS_DIR = 'gabbits'


def load_tests(loader, tests, pattern):
    """Provide a TestSuite to the discovery process."""
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    return driver.build_tests(test_dir, loader,
                              intercept=load_app,
                              )
