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
            spellFiles = listdir('game/spells')
            try:
                spellFiles.remove("__init__.py")
                spellFiles.remove("__pycache__")
            except ValueError:
                pass
            rendered_template = template.render(player=get(), db=db, sub=sub, spellFiles=spellFiles)
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
                append = False
                with open("game/spells/__init__.py", "r") as initF:
                    if json['spellFile'] not in initF.read():
                        append = True
                        pass
                if append:
                    with open("game/spells/__init__.py", "a") as initF:
                        initF.write("from ."+json['spellFile']+" import *")
                spells.insert_one(json)
            else: # request.method == 'GET'
                spellsJ = jsonify(spells.find())
                return spellsJ
        else:
            abort(404)
    except:
        abort(404)
