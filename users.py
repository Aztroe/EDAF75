from bottle import Bottle, get, post, run, request, response
import sqlite3
import hashlib
import json

db = sqlite3.connect('movies.sqlite')

users_app = Bottle()
USERS_ENDPOINT = '/users'

def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

@users_app.post('/')
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
            INTO customers
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
            db.commit()
            response.status = 201
            username, = found
            return f"{USERS_ENDPOINT}/{username}"
    except sqlite3.IntegrityError:
        response.status = 409
        return ""
    
@users_app.get('/<customer_username>/tickets')
def get_movies(customer_username):
    c = db.cursor()
    c.execute(
        """
        WITH users_tickets AS (
            SELECT performance_id
            FROM customers
                INNER JOIN tickets USING (username)
            WHERE username = ?
        )
        SELECT   start_date, start_time, theater_name, movie_title, movie_year, COUNT(performance_id)
        FROM     users_tickets
            LEFT JOIN performances USING (performance_id)
        GROUP BY performance_id
        """,
        [customer_username]

    )

    found = [{"date": start_date,
            "title": start_time,
            "theater": theater_name,
            "title": movie_title,
            "year":movie_year,
            "nbrOfTickets": count
            } 
            for start_date, start_time, theater_name, movie_title, movie_year, count in c]
    if len(found) == 0:
        response.status = 400
    return {"data": found}