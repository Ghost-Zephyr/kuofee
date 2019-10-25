#!/usr/bin/env python3
from flask import Flask, Response, jsonify, request, redirect, make_response, send_from_directory, abort
from flask_pymongo import PyMongo
from flask_cors import CORS
from os import path
from game import game, api, jwt, admin, err404, get

# ----- App init -----
jwt.keypair = jwt.set_keypair(jwt.read_keyfiles())

app = Flask(__name__)
CORS(app)

port = 8698
app.config['DEBUG'] = True
app.config['SERVE_STATIC'] = True
app.config['MONGO_DBNAME'] = "kuofee"
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/kuofee"
mongo = PyMongo(app)
db = mongo.db

# ----- Routes -----
@app.route("/", methods=['GET'])
def indexRoute():
    return game.index()

@app.route("/login", methods=['GET'])
def loginRoute():
    return game.login()

@app.route("/logout", methods=['GET'])
def logoutRoute():
    return jwt.forntendLogout()

@app.route("/register", methods=['GET'])
def registerRoute():
    return game.register()

@app.route("/about", methods=['GET'])
def aboutRoute():
    return game.about()

# --- Game Routes ---
@app.route("/player", methods=['GET'])
def playerRoute():
    return game.player()

# - Main Game View -
@app.route("/game", methods=['GET'])
def gameIndexRoute():
    return game.mainMenu(db)

# - Game screens -
@app.route("/game/q/<mode>", methods=['GET'])
def gameQpAI(mode):
    return game.qpAi(db, mode)

@app.route("/game/WalterPenny", methods=['GET'])
def gameWalterPennyRoute():
    return game.walterPenny()

# --- Game API ---
@app.route("/api/g/player", methods=['GET'])
def playerApiRoute():
    return api.player(db)

# ----- API Routes -----
@app.route("/api/p/register", methods=['POST'])
def registerApiRoute():
    return api.register(db)

@app.route("/api/p/login", methods=['POST'])
def loginApiRoute():
    return jwt.login(db)

@app.route("/api/p/logout", methods=['GET'])
def logoutApiRoute():
    return jwt.apiLogout()

# --- Admin API ---
@app.route("/api/a/spell", methods=['GET', 'POST'])
def adminSpellRoute():
    return admin.apiSpell(db)

# --- Admin Stuff ---
@app.route("/admin", methods=['GET'])
def adminRoute():
    return admin.index(db)

@app.route("/admin/<sub>", methods=['GET'])
def adminSubRoute(sub):
    return admin.sub(db, sub)

# --- Static Routes ---
@app.route("/admin/static/<path:path>", methods=['GET'])
def staticAdminRoute(path):
    try:
        jwt = get()
        if jwt['admin']:
            if app.config['SERVE_STATIC']:
                return send_from_directory('jinja2templates/admin/static', path)
            return redirect("/")
        else:
            abort(404)
    except:
        abort(404)

@app.route("/static/<path:path>", methods=['GET'])
def staticRoute(path):
    if app.config['SERVE_STATIC']:
        return send_from_directory('static', path)
    return redirect("/")

# --- Error handlers ---
@app.errorhandler(404)
def err404route(error=None):
    return err404(error)

if __name__ == "__main__":
    app.run(port=port)
