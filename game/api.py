from flask import jsonify, request, make_response
from authlib.jose import jwt as authlibjwt
import bcrypt
from .jwt import get, createToken

def newGame(db):
    try:
        jwt = get()
        new_game = {
            'type': 'ai',
            'player': {
                'nick': jwt['nick'],
                'HP': 777,
                'MP': 13
            }
        }
        goid = db.g.insert(new_game)
        db.p.update_one({
            { 'nick': jwt['nick'] },
            { '$set': { 'active_game': str(goid) } }
        })

        resp.status_code = 201
    except:
        resp = make_response("Could not create game.")
        resp.status_code = 500
        return resp

def player(db):
    try:
        players = db.p
        jwt = get()
        if jwt:
            player = players.find_one({ 'nick': jwt['nick'] })
            player['_id'] = str(player['_id'])
            player.remove('pwd')
            return jsonify(player)
        else:
            resp = make_response("Not logged in.")
            resp.status_code = 401
            return resp
    except:
        resp = make_response("Unknown error.")
        resp.status_code = 401
        return resp

def register(db):
    try:
        players = db.p
        if request.json:
            json = request.json
        else:
            json = request.form
        if json['pwd'] != json['pwd1']:
            resp = make_response("Passwords doesn't match!")
            resp.status_code = 406
            return resp
        elif players.find_one({ 'nick': json['nick'] }):
            resp = make_response("Nick taken.")
            resp.status_code = 409
            return resp
        else:
            players.insert_one({
                'nick': json['nick'],
                'pwd': bcrypt.hashpw(json['pwd'].encode('utf-8'), bcrypt.gensalt()),
                'admin': False,
                'pvestats': {},
                'pvpstats': {},
                'game': {},
                'deck': {},
                'collection': {}
            })
            token = createToken(db, json['nick'])
            resp = make_response("Created user and logged in.")
            resp.set_cookie("jwt", token, max_age=60*60*24*7)
            return resp
    except:
        resp = make_response("Could not create user.")
        resp.status_code = 400
        return resp
