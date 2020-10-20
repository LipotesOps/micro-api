# -*- coding: utf-8 -*-
"""pipeline views."""
from flask import Blueprint
from flask_login import login_required

blueprint = Blueprint("pipeline", __name__, url_prefix="/pipeline")


@blueprint.route("/")
def list():
    """List pipeline."""
    return render_template("users/members.html")
