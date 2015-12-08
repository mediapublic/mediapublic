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

Setting up Authentication
-------------------------
This step is not necessary unless you're working on stuff directly
related to auth. In order to fully mimic the production environment, it's great
to set up Twitter authentication. Here are the instructions for doing so:

1. Make your instance of mediapublic in your development environment public to the world
    - This can be done via a port forward to 6543 on your router.
    - This does not need to persist all of the time.  It only needs to be public if you want to use OAuth
2. Run your server
3. Go to https://apps.twitter.com/app/new
4. Put in `mediapublic as` the application name
5. Put in `Media Public Development Instance` for the description
6. Put in the github repo as the website: `https://github.com/mediapublic/mediapublic`
7. Put in `http://< your_external_ip >:6543/login` for the Callback URL
    - You'll need to know your external IP address.
    - You'll want to check to make sure that the link you put in produces the right page ( should just be a 'Login with twitter' link ).
8. Read the developers agreement, and if you agree, check the "Yes, I agree" check box.
9. Click "Create your Twitter application"
10. Once the Twitter application has been created, click the "Keys and Access Tokens".
    - Find the Consumer Key and Consumer Secret.
    - Set the appropriate keys in the development.ini file for `provider.twitter.consumer_key` and `provider.twitter.consumer_secret`
    - While you're in development.ini also set `mediapublic.ignore_authentication = false`
11. Restart the server with the new development.ini file secret keys loaded in.
12. Navigate to the client and click the "Login" button
    - Authorize mediapublic to access your twitter account
    - The login button should change to your name and a logout button!

***DO NOT COMMIT THESE KEYS TO GITHUB***

That should be it.  If you are not working on Twitter OAuth stuff, it is advised that you do not keep the application open to the world during development, as incremental builds may not be secure.

[gabbi]: http://gabbi.readthedocs.org/
[tox]: http://tox.testrun.org/
