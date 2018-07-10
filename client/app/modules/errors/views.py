# -*- coding: utf-8 -*-
"""Handle errors."""

from flask import render_template
from . import errors


@errors.app_errorhandler(404)
def page_not_found(e):
    """page_not_found."""
    return render_template('errors/errors.html', message=e), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    """internal_server_error."""
    return render_template('errors/errors.html', message=e), 500
