from .jinja import get, j2_env, render_game_template
from flask import request, abort

def index(db):
    try:
        jwt = get()
        if jwt['admin']:
            template = j2_env.get_template('admin/index.jinja2')
            rendered_template = template.render(player=get(), db=db)
            return rendered_template
        abort(404)
    except:
        abort(404)

def sub(db, sub):
    try:
        jwt = get()
        if jwt['admin']:
            template = j2_env.get_template('admin/sub.jinja2')
            rendered_template = template.render(player=get(), db=db, sub=sub)
            return rendered_template
        abort(404)
    except:
        abort(404)

def apiSpell(db):
    try:
        jwt = get()
        if jwt['admin']:
            spells = db.s
            if request.method == 'GET':
                spellsJ = jsonify(spells.find())
                return spellsJ
        abort(404)
    except:
        abort(404)
