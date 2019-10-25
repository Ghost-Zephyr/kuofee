from flask import jsonify, request, make_response
from authlib.jose import jwt as authlibjwt
from bcrypt import hashpw, gensalt, checkpw
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
            resp = make_response("Not signed in.")
            resp.status_code = 401
            return resp
    except:
        resp = make_response("Unknown error.")
        resp.status_code = 500
        return resp

def update(db):
    try:
        if request.json:
            json = request.json
        else:
            json = request.form
        updated = False
        jwt = get()
        if not jwt:
            resp = make_response("Not signed in!")
            resp.status_code = 401
            return resp
        player = db.p.find_one({ 'nick': jwt['nick'] })
        if checkpw(jwt['pwd'], player['pwd']):
            if checkpw(json['pwd'], player['pwd']):
                updated = []
                if json['nick']:
                    db.p.update_one(
                        { 'nick': player['nick'] },
                        { '$set': { 'nick': json['nick'] } }
                    )
                    updated.append("nick")
                resp = ""
                for update in updated:
                    resp += update+" "
                resp = make_response("Updated "+resp[0:-1])
                resp.status_code = 200
            else:
                resp = make_response("Wrong password!")
                resp.status_code = 403
                return resp
        else:
            resp = make_response("Not signed in!")
            resp.status_code = 401
            return resp
    except:
        if updated:
            resp = make_response("Updated only *"+updated+"* due to error")
            resp.status_code = 500
            return resp
        else:
            resp = make_response("Could not update!")
            resp.status_code = 500
            return resp

def register(db):
    try:
        if request.json:
            json = request.json
        else:
            json = request.form
        if db.p.find_one({ 'nick': json['nick'] }):
            resp = make_response("Nick taken.")
            resp.status_code = 409
            return resp
        try:
            if json['pwd'] != json['pwd1']:
                resp = make_response("Passwords doesn't match!")
                resp.status_code = 406
                return resp
        except KeyError:
            pass
        db.p.insert_one({
            'nick': json['nick'],
            'pwd': hashpw(json['pwd'].encode('utf-8'), gensalt()),
            'superadmin': False,
            'admin': False,
            'pvestats': {},
            'pvpstats': {},
            'game': {},
            'deck': {},
            'collection': {}
        })
        token = createToken(db, json['nick'])
        resp = make_response(token)
        resp.set_cookie("jwt", token, max_age=60*60*24*7)
        return resp
    except:
        resp = make_response("Could not create user.")
        resp.status_code = 500
        return resp
