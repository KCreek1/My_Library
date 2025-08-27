# wishlist

from flask import Blueprint, render_template, request
from helpers import get_current_user, login_required
from models import Wishlist

bp = Blueprint("wishlist", __name__)

@bp.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    """ will return a list of books that the user has added to their wishlist with pagination"""      
    user = get_current_user()
    page = request.args.get('page', 1, type=int)
    per_page = 25
    books_query = Wishlist.query.filter_by(username_id=user.id).order_by(Wishlist.title.asc())
    pagination = books_query.paginate(page=page, per_page=per_page)
    books = pagination.items
    return render_template('wishlist.html', books=books, user=user, pagination=pagination)

def register_routes(app):
    app.register_blueprint(bp)
