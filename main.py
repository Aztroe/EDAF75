from bottle import Bottle, get, post, run, request, response
import sqlite3

PORT = 7007
db = sqlite3.connect('movies.sqlite')

from movies import movies_endpoint
# from users import users_endpoint

main = Bottle()
main.mount('/movies', movies_endpoint)
# main.mount('/users', users_endpoint)

@main.get('/ping')
def ping():

    response.status = 200
    return {"data": "pong"}

@main.post('/reset')
def reset():
    c = db.cursor()
    c.execute(
        """
        DELETE FROM ticket;
        """
    )
    c.execute(
        """
        DELETE FROM screening;
        """
    )
    c.execute(
        """
        DELETE FROM customer;
        """
    )
    c.execute(
        """
        DELETE FROM movie;
        """
    )
    c.execute(
        """
        DELETE FROM theater;
        """
    )
    c.execute(
        """
        INSERT
        INTO   theater(theater_name, capacity)
        VALUES ('Regal', 16),
               ('Kino',       10),
               ('Skandia',     100);
        """
    )
    #TODO db.commit() -> sqlite3.OperationalError: disk I/O error 
    # ksk att main.py inte får modifiera movies.sqlite filen
    response.status = 200

@main.get('/theaters') # TEST THAT /reset WORKS
def get_theaters():
    c = db.cursor()
    c.execute(
        """
        SELECT   *
        FROM     theater
        """
    )
    response.status = 200
    found = [{"theaterName": theater_name,
              "capacity": capacity} 
              for theater_name, capacity in c]
    return {"data": found}


if __name__ == "__main__":
    run(main, host='localhost', port=PORT)