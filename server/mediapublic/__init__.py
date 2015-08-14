from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.events import NewRequest
from pyramid.settings import asbool

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
    config.include('cornice')

    # Set promiscuous CORS headers in the development environment
    if not settings['production_deployment']:
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    config.scan('mediapublic.views')

    return config.make_wsgi_app()


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers':
            'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)
