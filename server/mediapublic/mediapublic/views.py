import logging

from cornice import Service

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

log = logging.getLogger(name="mediapublic.{}".format(__name__))

########### STATUS CHECK
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

########### USERS
users = Service(name='users', path='/users')

# [GET, POST             ] /users
user = Service(name='user', path='/users/:{id}')
# [GET,       PUT, DELETE] /users/:{id}

########### USER TYPES
# [GET, POST             ] /user_types
# [GET,       PUT, DELETE] user_types/:id
########### RECORDING CATEGORIES
# [GET, POST             ] /recording_categories
# [GET,       PUT, DELETE] /recording_categories/:{id}
########### ORGANIZATIONS
# [GET, POST             ] /organizations
# [GET,       PUT, DELETE] /organizations/:{id}
# [GET, POST             ] /organization/:{oid}/comments
# [GET,       PUT, DELETE] /organization/:{oid}/comments/:{id}
########### PEOPLE                                                                                                                                     [14/42]
# [GET,                  ] /people
# [GET, POST             ] /organization/:{id}/people
# [GET,       PUT, DELETE] organization/:{oid}/people/:{pid}
# [GET, POST             ] organization/:{oid}/people/:{pid}/comments
# [GET,       PUT, DELETE] organization/:{oid}/people/:{pid}/comments/:{cid}
########### RECORDINGS
# [GET,                  ] /recordings
# [GET, POST             ] /organization/:{id}/recordings
# [GET,       PUT, DELETE] organization/:{oid}/recordings/:{id}
# [GET, POST             ] organization/:{oid}/recordings/:{rid}/comments
# [GET,       PUT, DELETE] organization/:{oid}/recordings/:{pid}/comments/:{id}
########### HOWTOS
# [GET, POST             ] /howtos
# [GET,       PUT, DELETE] /howtos/:{id}
# [GET, POST             ] /howtos/:{hid}/comments
# [GET,       PUT, DELETE] /howtos/:{hid}/comments/:{id}
########### BLOGS
# [GET, POST             ] /blogs
# [GET,       PUT, DELETE] /blogs/:{id}
# [GET, POST             ] /blogs/:{bid}/comments
# [GET,       PUT, DELETE] /blogs/:{bid}/comments/:{id}
########### PLAYLISTS
# [GET,                  ] /playlists
# [GET, POST,            ] /users/:{uid}/playlists
# [           PUT,       ] /users/:{uid}/playlists/:{id}/assign
# [           PUT,       ] /users/:{uid}/playlists/:{id}/remove
# [GET,       PUT, DELETE] /users/:{uid}/playlists/{:id}
