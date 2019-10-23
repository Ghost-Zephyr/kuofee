from flask import jsonify, request, make_response
from authlib.jose import jwt as authlibjwt
import bcrypt
from .jwt import get, createToken

def player(db):
    players = db.p
    token = get()
    if token:
        player = players.find_one({ 'nick': token['nick'] })
        player['_id'] = str(player['_id'])
        player.pop('pwd')
        return jsonify(player)
    else:
        resp = make_response("Not logged in.")
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
                'admin': 0,
                'pvestats': {},
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
