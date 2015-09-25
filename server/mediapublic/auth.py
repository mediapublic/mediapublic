import json
import logging

from cornice import Service
from pyramid import (
    authentication,
    authorization,
    security,
)

import requests

from .constants import cors_policies
from .models import Users

log = logging.getLogger(name="mediapublic.{}".format(__name__))


resource_acl = [
    (security.Allow, security.Everyone, 'get'),
    (security.Allow, 'group:writers', 'create'),
    (security.Allow, 'group:writers', 'update'),
    (security.Allow, 'group:admins', 'delete'),
]


def default_acl(request):
    pass


def users_acl(request):
    if request.authenticated_userid:
        pass


def associate_groups(user_id, request):
    # TODO(ryansb): maybe we need more than one group type.
    return 'user',


authn_policy = authentication.AuthTktAuthenticationPolicy(
    # TODO(ryansb): load this from config
    'secretsecrets',
    callback=associate_groups,
    hashalg='sha512',
)


authz_policy = authorization.ACLAuthorizationPolicy()


# --------- Auth and login
login = Service(name='login', path='/login', description="Auth and such")


@login.get(renderer="mediapublic:templates/login.jinja2", **cors_policies)
def login_form(request):
    print(request.params)
    return {"foo": "bar"}


@login.post(renderer="mediapublic:templates/logged_in.jinja2", **cors_policies)
def logged_in(request):
    log.debug("Received auth, token ID %s" % request.params['token'])
    resp = requests.get(request.host_url + '/auth/auth_info', params={
        'format': 'json',
        'token': request.params['token'],
    })
    # Future feature: when using providers other than twitter, check
    # auth_info['provider_name'] to see where the account is from
    auth_info = resp.json()
    twitter_handle = auth_info["profile"]["accounts"][0]['username']
    log.debug("Login for @%s" % twitter_handle)

    log.debug("Auth data: %s" % json.dumps(auth_info, indent=4))
    already_exists, uid = Users.update_social_login(twitter_handle, auth_info)

    log.debug("Succesfully authenticated @%s with twitter, exists:%s" %
              (twitter_handle, already_exists))

    principals = security.remember(request, str(uid))
    request.response.headerlist.extend(principals)
    log.debug("User authenticated, sending back %s" %
              request.response.headers)

    return {'exists': already_exists, 'handle': twitter_handle}


@login.delete(**cors_policies)
def logout(request):
    principals = security.forget(request)
    request.response.headerlist.extend(principals)
    return {"success": True}
