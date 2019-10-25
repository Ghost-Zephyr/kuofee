from .jinja import get, j2_env, render_game_template
from flask import request, abort
from os import listdir

# --- Views ---
def index(db):
    try:
        jwt = get()
        if jwt['admin']:
            template = j2_env.get_template('admin/index.jinja2')
            players = []
            for player in db.p.find():
                if player['superadmin']:
                    title = "Superadmin"
                elif player['admin']:
                    title = "Admin"
                else:
                    title = "Spellcaster"
                players.append({
                    'nick': player['nick'],
                    'pwd': player['pwd'],
                    'title': title
                })
            rendered_template = template.render(player=get(), db=db, players=players)
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

# --- API ---
def apiPlayers(db):
    try:
        jwt = get()
        if jwt['admin']:
            ps = {}
            for player in players.find():
                ps['nick'] = {
                    'pwd': player['pwd'],
                    'admin': player['admin'],
                    'pvestats': player['pvestats'],
                    'pvpstats': player['pvpstats'],
                    'game': player['game'],
                    'deck': player['deck'],
                    'collection': player['collection']
                }
            return jsonify(ps)
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
