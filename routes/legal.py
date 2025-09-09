from flask import Blueprint, render_template

bp = Blueprint('legal', __name__)

@bp.route("/privacy")
def privacy():
    return render_template("privacy.html")

@bp.route("/terms")
def terms():
    return render_template("terms.html")
