import logging
import json
import datetime


from cornice import Service
from cornice.schemas import validate_colander_schema
from cornice.resource import resource
from cornice.resource import view
import pyramid.security

from .auth import choose_context
from .constants import cors_policy
from .models import (
    Blogs,
    Comments,
    DBSession,
    HelpRequests,
    Howtos,
    Organizations,
    PlaylistAssignments,
    Playlists,
    RecordingCategories,
    Recordings,
    UserTypes,
    Users,
    SocialMedias,
)
from .validators import validator_from_model


log = logging.getLogger(name="mediapublic.{}".format(__name__))


class ResourceMixin(object):
    cls = None

    def __init__(self, request, context):
        self.request = request
        self.context = context

    @property
    def rsrc(self):
        return self.cls.__name__.lower()

    def validate_req(self, request):
        validate_colander_schema(validator_from_model(self.cls), request)

    @view(permission='get')
    def collection_get(self):
        log.debug("collection_get on {}".format(self.rsrc))
        return {
            'data': [i.to_dict() for i in self.cls.get_all()]
        }

    @view(validators=('validate_req', ), permission='create')
    def collection_post(self):
        log.debug("collection_post on {} with {}".format(
            self.rsrc, json.dumps(self.request.validated)))
        self.request.validated['creation_datetime'] = datetime.datetime.now()
        item = self.cls.add(**self.request.validated)
        self.request.response.status = 201
        return item.to_dict()

    @view(permission='get')
    def get(self):
        oid = self.request.matchdict['id']
        try:
            item = self.cls.get_by_id(oid)
            if item is None:
                self.request.response.status = 404
                return {'error': 'Not found'}
            return item.to_dict()
        except ValueError as e:
            log.warn("Invalid UUID {} passed.".format(oid))
            self.request.response.status = 400
            return {'error': 'Invalid UUID "{}" passed,'.format(oid) +
                    ' please fix it and try again'}
        else:
            return {}

    @view(permission='update', validators=('validate_req', ))
    def put(self):
        item = self.cls.update_by_id(
            self.request.matchdict['id'],
            **self.request.validated)

        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}

        self.request.response.status = 201
        return item.to_dict()

    @view(permission='delete')
    def delete(self):
        item = self.cls.delete_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

# --------- STATUS CHECK
status = Service(name='status', path='/status', description="Check app state",
                 cors_policy=cors_policy)


@status.get(permission=pyramid.security.NO_PERMISSION_REQUIRED)
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


@resource(collection_path='/users', path='/users/{id}',
          factory=choose_context, cors_policy=cors_policy)
class UsersResource(ResourceMixin):
    """
    [GET, POST             ] /users
    [GET,       PUT, DELETE] /users/{id}
    """
    cls = Users


@resource(collection_path='/social_medias', path='/social_medias/{id}',
          factory=choose_context, cors_policy=cors_policy)
class SocialMediasResource(ResourceMixin):
    """
    [GET, POST             ] /social_medias
    [GET,       PUT, DELETE] /social_medias/{id}
    """
    cls = SocialMedias


@resource(collection_path='/user_types', path='/user_types/{id}',
          factory=choose_context, cors_policy=cors_policy)
class UserTypesResource(ResourceMixin):
    """
    [GET, POST             ] /user_types
    [GET,       PUT, DELETE] /user_types/:id
    """
    cls = UserTypes


@resource(collection_path='/recording_categories',
          path='/recording_categories/{id}',
          factory=choose_context,
          cors_policy=cors_policy)
class RecordingCategoriesResource(ResourceMixin):
    """
    [GET, POST             ] /recording_categories
    [GET,       PUT, DELETE] /recording_categories/{id}
    """
    cls = RecordingCategories


@resource(collection_path='/organizations',
          path='/organizations/{id}',
          factory=choose_context,
          cors_policy=cors_policy)
class OrganizationsResource(ResourceMixin):
    """
    [GET, POST             ] /organizations
    [GET,       PUT, DELETE] /organizations/{id}
    """
    cls = Organizations


@resource(collection_path='/recordings',
          path='/recordings/{id}',
          factory=choose_context,
          cors_policy=cors_policy)
class RecordingsResource(ResourceMixin):
    """
    [GET, POST             ] /recordings
    [GET,       PUT, DELETE] /recordings/{id}
    """
    cls = Recordings


@resource(collection_path='/howtos',
          path='/howtos/{id}',
          factory=choose_context,
          cors_policy=cors_policy)
class HowtosResource(ResourceMixin):
    """
    [GET, POST             ] /howtos
    [GET,       PUT, DELETE] /howtos/{id}
    """
    cls = Howtos


@resource(collection_path='/help-requests',
          path='/help-requests/{id}',
          factory=choose_context,
          cors_policy=cors_policy)
class HelpRequests(ResourceMixin):
    """
    [GET, POST             ] /help-requests
    [GET,       PUT, DELETE] /help-requests/{id}
    """
    cls = HelpRequests


@resource(collection_path='/blogs', path='/blogs/{id}',
          factory=choose_context, cors_policy=cors_policy)
class BlogsResource(ResourceMixin):
    """
    [GET, POST             ] /blogs
    [GET,       PUT, DELETE] /blogs/{id}
    """
    cls = Blogs


@resource(collection_path='/playlists', path='/playlists/{id}',
          factory=choose_context, cors_policy=cors_policy)
class Playlists(ResourceMixin):
    """
    [GET, POST             ] /playlists
    [GET,       PUT, DELETE] /playlists/{id}
    """
    cls = Playlists
