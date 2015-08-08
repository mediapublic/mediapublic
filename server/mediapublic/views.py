import logging
import json
import datetime

from colander import MappingSchema
from cornice import Service
from cornice.resource import resource, view

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

log = logging.getLogger(name="mediapublic.{}".format(__name__))


class ResourceMixin(object):
    cls = None

    def __init__(self, request):
        self.request = request

    @property
    def rsrc(self):
        return self.cls.__name__.lower()

    def validate_req(self, request):
        v = validator_from_model(self.cls)

    def collection_get(self):
        log.debug("collection_get on {}".format(self.rsrc))
        return {
            self.rsrc: [i.to_dict() for i in self.cls.get_all()]
        }

    @property
    def schema(self):
        return validator_from_model(self.cls)

    @view(content_type="application/json")
    def collection_post(self):
        log.debug("collection_post on {} with {}".format(
            self.rsrc, json.dumps(self.request.validated)))
        self.request.validated['creation_datetime'] = datetime.datetime.now()
        item = self.cls.add(**self.request.validated)
        self.request.response.status = 201
        return item.to_dict()

    def get(self):
        item = self.cls.get_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

    def put(self):
        item = cls.update_by_id(
            self.request.matchdict['id'],
            **self.request.validated)

        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}

        self.request.response.status = 201
        return thing.to_dict()

    def delete(self):
        item = self.cls.delete_by_id(self.request.matchdict['id'])
        if item is None:
            self.request.response.status = 404
            return {'error': 'Not found'}
        return item.to_dict()

# --------- STATUS CHECK
status = Service(name='status', path='/status', description="Check app state")


@status.get()
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

# --------- USERS
# [GET, POST             ] /users
# [GET,       PUT, DELETE] /users/:{id}


@resource(collection_path='/users', path='/users/{id}')
class UserResource(ResourceMixin):
    cls = Users

# --------- USER TYPES
# [GET, POST             ] /user_types
# [GET,       PUT, DELETE] user_types/:id
# --------- RECORDING CATEGORIES
# [GET, POST             ] /recording_categories
# [GET,       PUT, DELETE] /recording_categories/:{id}
# --------- ORGANIZATIONS
# [GET, POST             ] /organizations
# [GET,       PUT, DELETE] /organizations/:{id}
# [GET, POST             ] /organization/:{oid}/comments
# [GET,       PUT, DELETE] /organization/:{oid}/comments/:{id}
# --------- PEOPLE
# [GET,                  ] /people
# [GET, POST             ] /organization/:{id}/people
# [GET,       PUT, DELETE] organization/:{oid}/people/:{pid}
# [GET, POST             ] organization/:{oid}/people/:{pid}/comments
# [GET,       PUT, DELETE] organization/:{oid}/people/:{pid}/comments/:{cid}
# --------- RECORDINGS
# [GET,                  ] /recordings
# [GET, POST             ] /organization/:{id}/recordings
# [GET,       PUT, DELETE] organization/:{oid}/recordings/:{id}
# [GET, POST             ] organization/:{oid}/recordings/:{rid}/comments
# [GET,       PUT, DELETE] organization/:{oid}/recordings/:{pid}/comments/:{id}
# --------- HOWTOS
# [GET, POST             ] /howtos
# [GET,       PUT, DELETE] /howtos/:{id}
# [GET, POST             ] /howtos/:{hid}/comments
# [GET,       PUT, DELETE] /howtos/:{hid}/comments/:{id}
# --------- BLOGS
# [GET, POST             ] /blogs
# [GET,       PUT, DELETE] /blogs/:{id}
# [GET, POST             ] /blogs/:{bid}/comments
# [GET,       PUT, DELETE] /blogs/:{bid}/comments/:{id}
# --------- PLAYLISTS
# [GET,                  ] /playlists
# [GET, POST,            ] /users/:{uid}/playlists
# [           PUT,       ] /users/:{uid}/playlists/:{id}/assign
# [           PUT,       ] /users/:{uid}/playlists/:{id}/remove
# [GET,       PUT, DELETE] /users/:{uid}/playlists/{:id}
