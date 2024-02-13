from bottle import Bottle, get, post, run, request, response
import sqlite3

PORT = 7007
db = sqlite3.connect('movies.sqlite')

from movies import movies_app, MOVIES_ENDPOINT
from users import users_app, USERS_ENDPOINT
from performances import performances_app, PERFORMANCES_ENDPOINT
from tickets import tickets_app, TICKETS_ENDPOINT

main = Bottle()
main.mount(MOVIES_ENDPOINT,     movies_app)
main.mount(USERS_ENDPOINT,      users_app)
main.mount(PERFORMANCES_ENDPOINT, performances_app)
main.mount(TICKETS_ENDPOINT,    tickets_app)

@main.get('/ping')
def ping():
    return "pong"

@main.post('/reset')
def reset():
    c = db.cursor()
    c.execute(
        """
        DELETE FROM tickets;
        """
    )
    c.execute(
        """
        DELETE FROM performances;
        """
    )
    c.execute(
        """
        DELETE FROM customers;
        """
    )
    c.execute(
        """
        DELETE FROM movies;
        """
    )
    c.execute(
        """
        DELETE FROM theaters;
        """
    )
    c.execute(
        """
        INSERT
        INTO   theaters(theater_name, capacity)
        VALUES ('Regal', 16),
               ('Kino',       10),
               ('Skandia',     100);
        """
    )
    db.commit()

@main.get('/theaters') # TEST THAT /reset WORKS
def get_theaters():
    c = db.cursor()
    c.execute(
        """
        SELECT   *
        FROM     theaters
        """
    )
    found = [{"theaterName": theater_name,
              "capacity": capacity} 
              for theater_name, capacity in c]
    return {"data": found}


if __name__ == "__main__":
    run(main, host='localhost', port=PORT)