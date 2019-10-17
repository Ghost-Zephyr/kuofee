#!/usr/bin/env python3
from werkzeug.security import safe_str_cmp
from flask import Flask, Response, jsonify, request, redirect, make_response
from flask_pymongo import PyMongo
from flask_cors import CORS
from game import *

# ----- App init -----
jwt.keypair = jwt.set_keypair(jwt.read_keyfiles())

app = Flask(__name__)
CORS(app)

port = 8080
app.config['DEBUG'] = True

url = "kuofee.sivert.pw"
app.config['MONGO_DBNAME'] = "kuofee"
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/kuofee"
mongo = PyMongo(app)
db = mongo.db

# ----- Routes -----
@app.route("/", methods=['GET'])
def indexRoute():
    return game.index(url)

@app.route("/login", methods=['GET'])
def loginRoute():
    return game.login(url)

@app.route("/static/<path:path>", methods=['GET'])
def staticRoute(path):
    return redirect("/")

# ----- API Routes -----
@app.route("/api/p/register", methods=['POST'])
def registerApiRoute():
    return jwt.register(db)

@app.route("/api/p/login", methods=['POST'])
def loginApiRoute():
    return jwt.login(db)

@app.route("/api/p/logout", methods=['GET'])
def logoutApiRoute():
    return jwt.logout()

# --- Game API ---
@app.route("/api/g/player", methods=['GET'])
def playerRoute():
    return api.player(db)

# --- Error handlers ---
@app.errorhandler(404)
def err404route(error=None):
    return err404(url, error)

if __name__ == "__main__":
    app.run(port=port)
