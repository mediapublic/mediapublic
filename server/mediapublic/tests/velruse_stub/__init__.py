from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

auth_info_json = open('auth_info.json', 'r').read()
login_twitter_json = open('login_twitter.json', 'r').read()


def auth_info(request):
    return Response(auth_info_json)


def login_twitter(request):
    return Response(login_twitter_json)


if __name__ == '__main__':

    config = Configurator()

    # configure the routes
    config.add_route('/auth_info', '/auth_info')
    config.add_view(auth_info, route_name='/auth_info')

    config.add_route('/login/twitter', '/login/twitter')
    config.add_view(login_twitter, route_name='/login/twitter')

    app = config.make_wsgi_app()

    server = make_server('127.0.0.1', 6544, app)
    server.serve_forever()
