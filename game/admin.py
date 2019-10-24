from .jinja import get, render_game_template
from flask import abort

def index(db):
    try:
        jwt = get()
        if jwt['admin']:
            return render_game_template('admin/index.jinja2', db)
    except:
        abort(404)
