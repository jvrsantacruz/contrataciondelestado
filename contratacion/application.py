# -*- coding: utf-8 -*-

from flask.ext import restful
from flask import Flask, Blueprint, current_app, g

from .models import get_scoped_session


def create_app(**kwargs):
    app = Flask('contratacion')

    if kwargs.get('debug'):
        app.debug = True

    setup_configuration(app, kwargs.get('config'))
    setup_api_handlers(app)
    setup_database_session(app)
    return app


def setup_api_handlers(app):
    from .api import api_blueprint
    app.register_blueprint(api_blueprint)


def setup_database_session(app):
    @app.before_request
    def setup_session(exception=None):
        g.db = get_scoped_session(current_app.config['DATABASE'])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if getattr(g, 'db', None) is not None:
            g.db.remove()


def setup_configuration(app, data):
    if data is None:
        app.config.from_envvar('CONTRATACION_CONFIG')
    elif isinstance(data, basestring):
        app.config.from_pyfile(data)
    else:
        app.config.update(data)
