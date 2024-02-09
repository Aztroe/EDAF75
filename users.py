from bottle import Bottle, get, post, run, request, response
import sqlite3
import hashlib
import json

db = sqlite3.connect('movies.sqlite')

users_endpoint = Bottle()

def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@users_endpoint.post('/')
def create_user():
    c = db.cursor()
    data = request.json
    username = data.get('username')
    fullName = data.get('fullName')
    password = data.get('pwd')
    hashedPassword = hash(password)
    
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO customer
            VALUES (?, ?, ?)
            RETURNING username
            """,
            [username, fullName, hashedPassword]
        )
        found = c.fetchone()
        if not found:
            response.status = 400
            return "Bad Request"
        else:
            # db.commit()
            response.status = 201
            username, = found
            return f"/users/{username}"
    except sqlite3.IntegrityError:
        response.status = 409
        return "Username already exists!"