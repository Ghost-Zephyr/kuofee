from flask import jsonify, request, make_response
from bcrypt import checkpw
from .jwt import get

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
