from .jinja import get, j2_env, render_game_template
from flask import request, abort
from os import listdir

def index(db):
    try:
        jwt = get()
        if jwt['admin']:
            template = j2_env.get_template('admin/index.jinja2')
            rendered_template = template.render(player=get(), db=db)
            return rendered_template
        else:
            abort(404)
    except:
        abort(404)

def sub(db, sub):
    try:
        jwt = get()
        if jwt['admin']:
            template = j2_env.get_template('admin/sub.jinja2')
            rendered_template = template.render(player=get(), db=db, sub=sub, spellFiles=listdir('game/spells'))
            return rendered_template
        else:
            abort(404)
    except:
        abort(404)

def apiSpell(db):
    try:
        jwt = get()
        if jwt['admin']:
            spells = db.s
            if request.method == 'POST':
                if request.json:
                    json = request.json
                else:
                    json = request.form
                spells.insert_one(json)
            else:
                spellsJ = jsonify(spells.find())
                return spellsJ
        else:
            abort(404)
    except:
        abort(404)
