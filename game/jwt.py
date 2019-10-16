from datetime import datetime, timedelta
from flask import request, make_response
from authlib.jose import jwt
import bcrypt

keypair = {}

def set_keypair(keys):
    keypair = {
        'private': keys[0],
        'public': keys[1]
    }
    return keypair

def read_keyfiles():
    prvkf = open("key.prv", "r")
    pubkf = open("key.pub", "r")
    try:
        b = prvkf.read(1)
        private_key = b
        while b != "":
            b = prvkf.read(1)
            private_key += b
        b = pubkf.read(1)
        public_key = b
        while b != "":
            b = pubkf.read(1)
            public_key += b
    except:
        print("\033[3mCould not read key files!\033[0m")
        exit()
    finally:
        prvkf.close()
        pubkf.close()
    return private_key, public_key

def register(db):
    return NotImplementedError

def login(db):
    try:
        try:
            pJ = request.json['p']
        except KeyError:
            resp = make_response("No player.")
            resp.status_code = 400
            return resp
        p = db.p.find_one({ "nick": pJ['nick'] })
        if bcrypt.checkpw(pJ['pwd'].encode('utf-8'), p['pwd']):
            exp = datetime.utcnow() + timedelta(days=7)
            token = jwt.encode({'alg': 'RS256'}, {
                'nick': pJ['nick'],
                'admin': pJ['admin'],
                'exp': exp,
            }, jwt_keypair['private'])
            resp = make_response("Token created.")
            resp.set_cookie("token", token, max_age=60*60*24*7)
            return resp
        else:
            resp = make_response("Wrong password!")
            resp.status_code = 401
            return resp
    except:
        resp = make_response("Could not create token.")
        resp.status_code = 500
        return resp

def check():
    try:
        dec = jwt.decode(request.cookies.get('token'), jwt_keypair['public'])
        dec.validate()
        return dec
    except:
        return -1
