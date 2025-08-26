# error handling routes
from flask import current_app, request
from helpers import apology

def page_not_found(e):
    current_app.logger.error(f"404 Error: {e}, Route: {request.url}")
    return apology("Page not found", 404)

def internal_error(e):
    current_app.logger.error(f"500 Error: {e}, Route: {request.url}")
    return apology("Internal server error", 500)