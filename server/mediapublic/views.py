import logging
import json
import datetime
import functools


from cornice import Service
from cornice.schemas import validate_colander_schema
from cornice.resource import resource
import pyramid.security

from .auth import resource_acl
from .constants import cors_policies
from .models import (
    Blogs,
    Comments,
    DBSession,
    Howtos,
    Organizations,
    People,
    PlaylistAssignments,
    Playlists,
    RecordingCategories,
    Recordings,
    UserTypes,
    Users,
)
from .validators import validator_from_model

from cornice.resource import view as raw_view

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

    __acl__ = resource_acl

    @property
    def rsrc(self):
        return self.cls.__name__.lower()

    def validate_req(self, request):
        validate_colander_schema(validator_from_model(self.cls), request)

    @view(permission=pyramid.security.NO_PERMISSION_REQUIRED)
    def collection_get(self):
        log.debug("collection_get on {}".format(self.rsrc))
        print(self._services.get('collection_usersresource'))
        print(self.request.__dict__['matched_route'])
        return {
            self.rsrc: [i.to_dict() for i in self.cls.get_all()]
        }

    @view(validators=('validate_req', ), permission='create')
    def collection_post(self):
        log.debug("collection_post on {} with {}".format(
            self.rsrc, json.dumps(self.request.validated)))
        self.request.validated['creation_datetime'] = datetime.datetime.now()
        item = self.cls.add(**self.request.validated)
        self.request.response.status = 201
        return item.to_dict()

    @view(permission=pyramid.security.NO_PERMISSION_REQUIRED)
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
