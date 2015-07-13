from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

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
    )

import datetime
import json

def check_payload(body, cls):

    dt_objs = [
        'creation_datetime',
        'edit_datetime',
        'recorded_datetime',
    ]

    payload = {}
    resp = None
    #code = 200
    try:
        payload = json.loads(body)
        if not isinstance(payload, dict):
            payload = {}
            resp = {'error': 'JSON not dictionary.'}
            #code = 400
        else:
            keys = cls.reqkeys()
            if not ( len(keys) == len(payload) and all(k in payload for k in keys) ):
                payload = {}
                resp = {'error': 'Missing Key.  Required Keys: %s' % cls.reqkeys()}
                #code = 400
            else:
                for k in payload:
                    if k in dt_objs:
                        try:
                            payload[k] = datetime.datetime.strptime(payload[k], "%Y-%m-%d %H:%M:%S.%f")
                        except:
                            payload = {}
                            resp = {'error': 'Invalid DateTime format for key: %s' % k}
                            break
    except:
        resp = {'error': 'Invalid JSON'}
    #    #code = 400

    return payload, resp #, code

def do_post(request, keys, cls,):
    resp = {'error': 'Invalid Input'}
    status = 400
    payload, err = check_payload(request.body, cls)
    if err is None:
        for k in keys:
            payload[k] = keys[k]
        payload['creation_datetime'] = datetime.datetime.now()
        org = cls.add(**payload)
        resp = org.to_dict()
        status = 201
    else:
        resp = err
    return resp, status

def do_get_single(request, id, cls):
    resp = {'error': 'Not Found'}
    status = 404
    thing = cls.get_by_id(id)
    if not thing is None:
        resp = thing.to_dict()
        status = 200
    return resp, status
    
def do_put(request, id, cls):

    resp = {'error': 'Not Found'}
    status = 404
    payload, err = check_payload(request.body, cls)
    if err is None:
        thing = cls.update_by_id(id, **payload)
        if not thing is None:
            resp = thing.to_dict()
            status = 201
    else:
        resp = err
    return resp, status

def do_delete(request, id, cls):
    resp = {'error': 'Not Found'}
    status = 404
    thing = cls.delete_by_id(id)
    if not thing is None:
        resp = {}
        status = 204
    return resp, status

METHODS = {
    'GET': do_get_single,
    #'POST': do_post,
    'PUT': do_put,
    'DELETE': do_delete,
}

#@view_config(route_name='index', renderer='templates/index.mak')
#def view_indecx(request):
#
#    return {}
    
########### INDEX
#@view_config(route_name='index', '/', )

########### ABOUT
#@view_config(route_name='about', '/')



########### USERS

# [GET, POST             ] /users
@view_config(route_name='users', renderer='json')
def users(request):
    cls = Users
    resp = []
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] /users/:{id}
@view_config(route_name='user_by_id', renderer='json')
def user_by_id(request):
    cls = Users
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp



########### USER TYPES

# [GET, POST             ] /user_types
@view_config(route_name='user_types', renderer='json')
def user_types(request):
    cls = UserTypes
    resp = []
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] user_types/:id
@view_config(route_name='user_type_by_id', renderer='json')
def user_type_by_id(request):
    cls = UserTypes
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp



########### RECORDING CATEGORIES

# [GET, POST             ] /recording_categories
@view_config(route_name='recording_categories', renderer='json')
def recording_categories(request):
    cls = RecordingCategories
    resp = []
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp
    
# [GET,       PUT, DELETE] /recording_categories/:{id}
@view_config(route_name='recording_category_by_id', renderer='json')
def recording_category_by_id(request):
    cls = RecordingCategories
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp




########### ORGANIZTIONS

# [GET, POST             ] /organizations
@view_config(route_name='organizations', renderer='json')
def organizations(request):
    cls = Organizations
    resp = []
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] /organizations/:{id}
@view_config(route_name='organization_by_id', renderer='json')
def organization_by_id(request):
    cls = Organizations
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp

# [GET, POST             ] /organization/:{oid}/comments
@view_config(route_name='organizations_comments', renderer='json')
def organizations_comments(request):
    cls = Comments
    resp = []
    oid = request.matchdict['oid']
    if request.method == 'GET':
        items = cls.get_by_organization_id(oid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'organization_id': oid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] organization/:{oid}/comments/:{cid}
@view_config(route_name='organizations_comment_by_id', renderer='json')
def organizations_comment_by_id(request):
    cls = Comments
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp




########### PEOPLE

# [GET,                  ] /people
@view_config(route_name='people', renderer='json')
def people(request):
    cls = People
    resp = {}
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET, POST             ] /organization/:{id}/people
@view_config(route_name='organization_people', renderer='json')
def organization_people(request):
    cls = People
    resp = []
    oid = request.matchdict['oid']
    if request.method == 'GET':
        items = cls.get_by_organization_id(oid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'organization_id': oid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] organization/:{oid}/people/:{pid}
@view_config(route_name='organization_people_by_id', renderer='json')
def organization_people_by_id(request):
    cls = People
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp

# [GET, POST             ] organization/:{oid}/people/:{pid}/comments
@view_config(route_name='organization_people_comments', renderer='json')
def organization_people_comments(request):
    cls = Comments
    resp = []
    oid = request.matchdict['oid']
    pid = request.matchdict['pid']
    if request.method == 'GET':
        items = cls.get_by_people_id(oid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'people_id': pid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] organization/:{oid}/people/:{pid}/comments/:{cid}
@view_config(route_name='organization_people_comment_by_id', renderer='json')
def organization_people_comment_by_id(request):
    cls = Comments
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp


########### RECORDINGS

# [GET,                  ] /recordings
@view_config(route_name='recordings', renderer='json')
def recordings(request):
    cls = Recordings
    resp = {}
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET, POST             ] /organization/:{id}/recordings
@view_config(route_name='organization_recordings', renderer='json')
def organization_recordings(request):
    cls = Recordings
    resp = []
    oid = request.matchdict['oid']
    if request.method == 'GET':
        items = cls.get_by_organization_id(oid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'organization_id': oid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] organization/:{oid}/recordings/:{id}
@view_config(route_name='organization_recordings_by_id', renderer='json')
def organization_recordings_by_id(request):
    cls = Recordings
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp

# [GET, POST             ] organization/:{oid}/recordings/:{rid}/comments
@view_config(route_name='organization_recordings_comments', renderer='json')
def organization_recordings_comments(request):
    cls = Comments
    resp = []
    oid = request.matchdict['oid']
    rid = request.matchdict['rid']
    if request.method == 'GET':
        items = cls.get_by_recording_id(oid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'recording_id': rid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] organization/:{oid}/recordings/:{pid}/comments/:{id}
@view_config(route_name='organization_recordings_comment_by_id', renderer='json')
def organization_recordings_comment_by_id(request):
    cls = Comments
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp



########### HOWTOS

# [GET, POST             ] /howtos
@view_config(route_name='howtos', renderer='json')
def howtos(request):
    cls = Howtos
    resp = []
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] /howtos/:{id}
@view_config(route_name='howtos_by_id', renderer='json')
def howtos_by_id(request):
    cls = Howtos
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp

# [GET, POST             ] /howtos/:{hid}/comments
@view_config(route_name='howtos_comments', renderer='json')
def howtos_comments(request):
    cls = Comments
    resp = []
    hid = request.matchdict['hid']
    if request.method == 'GET':
        items = cls.get_by_howto_id(hid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'howto_id': hid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] /howtos/:{hid}/comments/:{id}
@view_config(route_name='howtos_comment_by_id', renderer='json')
def howtos_comment_by_id(request):
    cls = Comments
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp
    
    

########### BLOGS

# [GET, POST             ] /blogs
@view_config(route_name='blogs', renderer='json')
def blogs(request):
    cls = Blogs
    resp = []
    if request.method == 'GET':
        items = cls.get_all()
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {}
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] /blogs/:{id}
@view_config(route_name='blogs_by_id', renderer='json')
def blogs_by_id(request):
    cls = Blogs
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp

# [GET, POST             ] /blogs/:{bid}/comments
@view_config(route_name='blogs_comments', renderer='json')
def blogs_comments(request):
    cls = Comments
    resp = []
    bid = request.matchdict['bid']
    if request.method == 'GET':
        items = cls.get_by_blog_id(bid)
        resp = [i.to_dict() for i in items]
    elif request.method == 'POST':
        keys = {
            'blog_id': bid,
        }
        resp, status = do_post(request, keys, cls)
    else:
        resp = {'error': 'Method Not Allowed'}
        request.response.status = 405
    return resp

# [GET,       PUT, DELETE] /blogs/:{bid}/comments/:{id}
@view_config(route_name='blogs_comment_by_id', renderer='json')
def blogs_comment_by_id(request):
    cls = Comments
    resp = {}
    id = request.matchdict['id']
    if not request.method in METHODS:
        resp = {'error': 'Method Not Allowed'}
        status = 405
    else:
        resp, status = METHODS[request.method](request, id, cls)
    request.response.status = status
    return resp
