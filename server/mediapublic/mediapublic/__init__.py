from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.settings import asbool
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    production_deployment = asbool(settings.get(
        'production_deployment', 'false'))
    settings['production_deployment'] = production_deployment
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    # INDEX
    #config.add_route('index', '/')

    # ABOUT
    #config.add_route('about', '/')

    # USERS
    config.add_route('users', '/users')
    config.add_route('user_by_id', '/users/:{id}')

    # RECORDING CATEGORIES
    config.add_route('user_types', '/user_types')
    config.add_route('user_type_by_id', '/user_types/:{id}')

    # RECORDING CATEGORIES
    config.add_route('recording_categories', '/recording_categories')
    config.add_route('recording_category_by_id', '/recording_categories/:{id}')

    # ORGANIZTIONS
    config.add_route('organizations', '/organizations')
    config.add_route('organization_by_id', '/organizations/:{id}')
    config.add_route('organizations_comments', '/organizations/:{oid}/comments')
    config.add_route('organizations_comment_by_id', '/organizations/:{oid}/comments/:{id}')

    # PEOPLE
    config.add_route('people', '/people')
    config.add_route('organization_people', '/organizations/:{oid}/people')
    config.add_route('organization_people_by_id', '/organizations/:{oid}/people/:{id}')
    config.add_route('organization_people_comments', '/organizations/:{oid}/people/:{pid}/comments')
    config.add_route('organization_people_comment_by_id', '/organizations/:{oid}/people/:{pid}/comments/:{id}')

    # RECORDINGS
    config.add_route('recordings', '/recordings')
    config.add_route('organization_recordings', '/organizations/:{oid}/recordings')
    config.add_route('organization_recordings_by_id', '/organizations/:{oid}/recordings/:{id}')
    config.add_route('organization_recordings_comments', '/organizations/:{oid}/recordings/:{rid}/comments')
    config.add_route('organization_recordings_comment_by_id', '/organizations/:{oid}/recordings/:{rid}/comments/:{id}')

    # PLAYLISTS
    config.add_route('playlists', '/playlists')
    config.add_route('user_playlists', '/users/:{uid}/playlists')
    config.add_route('user_playlists_by_id', '/users/:{uid}/playlists/:{id}')
    config.add_route('user_playlists_assign', '/users/:{uid}/playlists/:{id}/assign')
    config.add_route('user_playlists_remove', '/users/:{uid}/playlists/:{id}/remove')

    # HOWTOS
    config.add_route('howtos', '/howtos')
    config.add_route('howtos_by_id', '/howtos/:{id}')
    config.add_route('howtos_comments', '/howtos/:{hid}/comments')
    config.add_route('howtos_comment_by_id', '/howtos/:{hid}/comments/:{id}')

    # BLOGS
    config.add_route('blogs', '/blogs')
    config.add_route('blogs_by_id', '/blogs/:{id}')
    config.add_route('blogs_comments', '/blogs/:{bid}/comments')
    config.add_route('blogs_comment_by_id', '/blogs/:{bid}/comments/:{id}')

    # Set promiscuous CORS headers in the development environment
    if (not settings['production_deployment']):
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    config.scan()
    return config.make_wsgi_app()


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)
