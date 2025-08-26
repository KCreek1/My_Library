# error handling routes
from flask import Blueprint, current_app, request
from helpers import apology

bp = Blueprint('errors', __name__)

# 404 Error Handler
@bp.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.error(f"404 Error: {e}, Route: {request.url}")  # Log with route
    return apology("Page not found", 404)

# 500 Error Handler
@bp.app_errorhandler(500)
def internal_error(e):
    current_app.logger.error(f"500 Error: {e}, Route: {request.url}")  # Log with route
    return apology("Internal server error", 500)