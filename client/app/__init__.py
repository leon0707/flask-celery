# -*- coding: utf-8 -*-
"""Flask project init."""


from flask import Flask
from flask.cli import AppGroup
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from celery import Celery
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
migrate = Migrate()
mail = Mail()
celery = Celery()

def create_app(config_name):
    """Create app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # group commands
    command_group_cli = AppGroup('command_group')
    app.cli.add_command(command_group_cli)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # celery
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

    # import blueprint
    from .modules.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from .modules.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .modules.task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/task')

    return app
