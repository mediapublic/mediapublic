import cornice.pyramidhook as hooks
from pyramid import authentication
from pyramid.config import Configurator
from pyramid import security
from sqlalchemy import engine_from_config
from pyramid import httpexceptions

from mediapublic import auth
from mediapublic import exceptions as mp_exc
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

    config.set_authentication_policy(
        authentication.AuthTktAuthenticationPolicy(
            config.get_settings().get('mediapublic.authentication_secret',
                                      'changeme'),
            callback=auth.associate_groups,
            hashalg='sha512',
        )
    )
    config.set_authorization_policy('mediapublic.auth.authz_policy')
    config.add_permission('get')
    config.add_permission('create')
    config.add_permission('update')
    config.add_permission('delete')

    config.include('cornice')
    config.scan('mediapublic.auth')
    config.scan('mediapublic.views')

    config.include('velruse.providers.twitter')

    config.add_view(mp_exc.handle_exceptions, context=Exception,
                    permission=security.NO_PERMISSION_REQUIRED)
    # TODO(ryansb): replace default 40(3|4) with JSON errors
    config.add_view(hooks.handle_exceptions,
                    context=httpexceptions.HTTPNotFound,
                    permission=security.NO_PERMISSION_REQUIRED)
    config.add_view(hooks.handle_exceptions,
                    context=httpexceptions.HTTPForbidden,
                    permission=security.NO_PERMISSION_REQUIRED)

    return config.make_wsgi_app()
