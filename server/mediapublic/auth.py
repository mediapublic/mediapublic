import json
import logging

from cornice import Service
from pyramid import (
    authentication,
    authorization,
    security,
)
from pyramid.httpexceptions import HTTPFound

import requests

from .constants import cors_policy
from .models import Users

log = logging.getLogger(name="mediapublic.{}".format(__name__))


default_acl = [
    (security.Allow, security.Everyone, 'get'),
    (security.Allow, 'group:admins', 'create'),
    (security.Allow, 'group:staff', 'create'),
    (security.Allow, security.Authenticated, 'create'),
    (security.Allow, 'group:admins', 'delete'),
    (security.Allow, 'group:admins', 'update'),
    (security.Allow, 'group:staff', 'delete'),
    (security.Allow, 'group:staff', 'update'),
]


class Context(object):
    def __init__(self, acl):
        """`acl` is a list of triples (result, principal, permission)"""
        self.__acl__ = acl[:]


def choose_context(request):
    # request.matched_route.name
    if request.registry.settings.get(
            'mediapublic.ignore_authentication'):
        return Context([
            (security.Allow, security.Everyone, 'get'),
            (security.Allow, security.Everyone, 'create'),
            (security.Allow, security.Everyone, 'update'),
            (security.Allow, security.Everyone, 'delete'),
        ])
    acl = default_acl[:]
    if ('usersresource' in request.matched_route.name and
            request.authenticated_userid):
        acl.append(
            (security.Allow, request.authenticated_userid, 'update')
        )
    return Context(acl)


def users_acl(request):
    if request.authenticated_userid:
        pass


def associate_groups(user_id, request):
    # TODO(ryansb): actually associate users/groups using the
    # UserTypes model
    return 'user', 'admin'


authn_policy = authentication.AuthTktAuthenticationPolicy(
    # TODO(ryansb): load this from config
    'secretsecrets',
    callback=associate_groups,
    hashalg='sha512',
)


authz_policy = authorization.ACLAuthorizationPolicy()


# --------- Auth and login
login = Service(name='login', path='/login',
                description="Auth and such",
                cors_policy=cors_policy)


@login.get(renderer="mediapublic:templates/login.jinja2")
def login_form(request):
    print(request.params)
    return {"foo": "bar"}


@login.post()
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

    log.debug(request.params)

    return HTTPFound(
        location=request.registry.settings['mediapublic.client_url'])


@login.delete()
def logout(request):
    principals = security.forget(request)
    request.response.headerlist.extend(principals)
    return {"success": True}
