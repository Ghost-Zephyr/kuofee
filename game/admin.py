from flask import abort
from .jinja import *
from .jwt import get

def index(db):
    try:
        jwt = get()
        if jwt['admin']:
            return render_game_template('admin/index.jinja2', db)
    except:
        abort(404)
