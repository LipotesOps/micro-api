# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from eve import Eve
from flask import render_template
from flask_graphql import GraphQLView
from graphene import ObjectType, Schema, String

from micro_ops import commands, public, user
from micro_ops.extensions import (
    bcrypt,
    cache,
    # csrf_protect,
    db,
    debug_toolbar,
    flask_static_digest,
    login_manager,
    migrate,
)
from micro_ops.event_hook import (
    init_register,
    update_schema,
    inserted_resource,
    updated_resource,
)


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return "Hello " + name

    def resolve_goodbye(root, info):
        return "See ya!"


schema = Schema(query=Query)


def create_app(config_object="micro_ops.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    # app = Flask(__name__.split(".")[0])
    app = Eve(settings="eve_settings.py")

    # init register resource
    with app.app_context():
        init_register()
        pass

    # app.on_post_POST_resource += update_schema
    # app.on_post_PATCH_resource += update_schema
    app.on_inserted_resource += inserted_resource
    app.on_updated_resource += updated_resource

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
    )

    # Optional, for adding batch query support (used in Apollo-Client)
    # app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql', schema=schema, batch=True))

    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    # csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
