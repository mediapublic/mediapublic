import logging
import json
import datetime
import functools

import requests

from cornice import Service
from cornice.schemas import validate_colander_schema
from cornice.resource import resource

from .models import (
    DBSession,
    Users,
    UserTypes,
    RecordingCategories,
    Comments,
    Organizations,
    People,
    Recordings,
    Howtos,
    Blogs,
    Playlists,
    PlaylistAssignments,
    )
from .validators import validator_from_model

from cornice.resource import view as raw_view

cors_policies = dict(
    cors_enabled=True,
    cors_origins=('*', ),
    cors_max_age=1728000,
    cors_headers=('Origin' 'Content-Type', 'Accept', 'Authorization'),
    cors_credentials=True,
)

view = functools.partial(
    raw_view,
    content_type="application/json",
    **cors_policies
)

log = logging.getLogger(name="mediapublic.{}".format(__name__))


class ResourceMixin(object):
    cls = None

    def __init__(self, request):
        self.request = request

    @property
    def rsrc(self):
        return self.cls.__name__.lower()

    def validate_req(self, request):
        validate_colander_schema(validator_from_model(self.cls), request)

    def collection_get(self):
        log.debug("collection_get on {}".format(self.rsrc))
        return {
            self.rsrc: [i.to_dict() for i in self.cls.get_all()]
        }

    @view(validators=('validate_req', ))
    def collection_post(self):
        log.debug("collection_post on {} with {}".format(
            self.rsrc, json.dumps(self.request.validated)))
        self.request.validated['creation_datetime'] = datetime.datetime.now()
        item = self.cls.add(**self.request.validated)
        self.request.response.status = 201
        return item.to_dict()

    @view()
    def get(self):
        item = self.cls.get_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

    @view(validators=('validate_req', ))
    def put(self):
        item = self.cls.update_by_id(
            self.request.matchdict['id'],
            **self.request.validated)

        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}

        self.request.response.status = 201
        return item.to_dict()

    @view()
    def delete(self):
        item = self.cls.delete_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

# --------- STATUS CHECK
status = Service(name='status', path='/status', description="Check app state")


@status.get(content_type='application/json', **cors_policies)
def get_status(request):
    log.debug("Status check")
    status = {'web': True}
    # get the current time from the DB to make sure our connection works
    status['database'] = bool(
        DBSession.connection().execute(
            "SELECT TIME('NOW')"
        ).fetchone()
    )
    if not all(status.values()):
        log.warn("Uhoh, status check failed {}".format(repr(status)))
    return status


@resource(collection_path='/users', path='/users/{id}')
class UsersResource(ResourceMixin):
    """
    [GET, POST             ] /users
    [GET,       PUT, DELETE] /users/{id}
    """
    cls = Users


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
    already_exists = Users.update_social_login(twitter_handle, auth_info)

    log.debug("Succesfully authenticated @%s with twitter, exists:%s" %
              (twitter_handle, already_exists))

    return {'exists': already_exists, 'handle': twitter_handle}


@resource(collection_path='/user_types', path='/user_types/{id}')
class UserTypesResource(ResourceMixin):
    """
    [GET, POST             ] /user_types
    [GET,       PUT, DELETE] /user_types/:id
    """
    cls = UserTypes


@resource(collection_path='/recording_categories',
          path='/recording_categories/{id}')
class RecordingCategoriesResource(ResourceMixin):
    """
    [GET, POST             ] /recording_categories
    [GET,       PUT, DELETE] /recording_categories/{id}
    """
    cls = RecordingCategories


@resource(collection_path='/organizations', path='/organizations/{id}')
class OrganizationsResource(ResourceMixin):
    """
    [GET, POST             ] /organizations
    [GET,       PUT, DELETE] /organizations/{id}
    """
    cls = Organizations

# --------- PEOPLE
# [GET, POST             ] /people
# [GET,       PUT, DELETE] /people/{id}
# --------- RECORDINGS
# [GET, POST             ] /recordings
# [GET,       PUT, DELETE] /recordings/{id}
# --------- HOWTOS
# [GET, POST             ] /howtos
# [GET,       PUT, DELETE] /howtos/{id}


@resource(collection_path='/blogs', path='/blogs/{id}')
class BlogsResource(ResourceMixin):
    """
    [GET, POST             ] /blogs
    [GET,       PUT, DELETE] /blogs/{id}
    """
    cls = Blogs


# --------- PLAYLISTS
# [GET, POST             ] /playlists
# [GET,       PUT, DELETE] /playlists/{id}
# [           PUT,       ] /playlists/{id}/assign
# [           PUT,       ] /playlists/{id}/remove
