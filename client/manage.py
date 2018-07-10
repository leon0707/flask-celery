# -*- coding: utf-8 -*-
"""Boilerplate for flask production."""
import click
import os
from flask_migrate import upgrade
from app import create_app, db
from flask.cli import AppGroup
from app.models import User


basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app(os.getenv('CONFIG_NAME') or 'default')
# group commands
command_group_cli = AppGroup('command_group')
app.cli.add_command(command_group_cli)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User)


if __name__ == '__main__':
    app.run()


@app.cli.command()
@click.argument('args')
def run_test(args):
    """Eg. `flask run_test hello`. Return: hello."""
    print args


@command_group_cli.command('test')
@click.argument('args')
def test_group_commends(args):
    """Eg. `flask command_group test hello`. Return: hello."""
    print args


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
