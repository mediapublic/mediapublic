from pyramid.config import Configurator
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
    config = Configurator(
        settings=settings,
    )

    config.set_authentication_policy('mediapublic.auth.authn_policy')
    config.set_authorization_policy('mediapublic.auth.authz_policy')
    config.add_permission('get')
    config.add_permission('create')
    config.add_permission('update')
    config.add_permission('delete')

    config.include('cornice')
    config.scan('mediapublic.auth')
    config.scan('mediapublic.views')

    config.include('velruse.providers.twitter')

    return config.make_wsgi_app()
