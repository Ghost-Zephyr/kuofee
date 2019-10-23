from datetime import datetime, timedelta
from flask import request, make_response, redirect
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
    try:
        prvkf = open("jwt-keys/key.pem", "r")
        pubkf = open("jwt-keys/key.pub", "r")
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
    return NotImplementedError # TODO:

def login(db):
    try:
        if request.json:
            json = request.json
        else:
            json = request.form
        p = db.p.find_one({ "nick": json['nick'] })
        if bcrypt.checkpw(json['pwd'].encode('utf-8'), p['pwd']):
            exp = datetime.utcnow() + timedelta(days=7)
            token = jwt.encode({'alg': 'RS256'}, {
                'nick': p['nick'],
                'admin': p['admin'],
                'exp': exp,
            }, keypair['private'])
            resp = make_response("Token created.")
            resp.set_cookie("jwt", token, max_age=60*60*24*7)
            return resp
        else:
            resp = make_response("Wrong password!")
            resp.status_code = 401
            return resp
    except:
        resp = make_response("Request error.")
        resp.status_code = 400
        return resp

def apiLogout():
    resp = make_response("Logged out.")
    resp.set_cookie("jwt", "", max_age=0)
    return resp

def forntendLogout():
    resp = redirect("/")
    resp.set_cookie("jwt", "", max_age=0)
    return resp

def get():
    try:
        dec = jwt.decode(request.cookies.get('jwt'), keypair['public'])
        dec.validate()
        return dec
    except:
        return False
