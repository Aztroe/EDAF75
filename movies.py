from bottle import Bottle, get, post, run, request, response
import sqlite3

db = sqlite3.connect('movies.sqlite')

movies_app = Bottle()
MOVIES_ENDPOINT = '/movies'

@movies_app.get('/')
def get_movies():
    c = db.cursor()
    c.execute(
        """
        SELECT   imdb_key, movie_title, movie_year
        FROM     movies
        """
    )
    response.status = 200
    found = [{"imdbKey": imdb_key,
              "title": title,
              "year": year} 
              for imdb_key, title, year in c]
    return {"data": found}

@movies_app.post('/')
def create_movie():
    data = request.json
    imdb_key = data.get('imdbKey')
    title = data.get('title')
    year = data.get('year')

    c = db.cursor()
    try:
        c.execute(
            """
            SELECT imdb_key FROM movies
            WHERE imdb_key = ?
            """,
            [imdb_key]
        )
        found = c.fetchone()
        if found:
            response.status = 400
            return ""
        else:
            c.execute(
                """
                INSERT
                INTO movies (imdb_key, movie_title, movie_year)
                VALUES (?, ?, ?)
                """,
                [imdb_key, title, year]
            )
            db.commit()
            response.status = 201
        return f"{MOVIES_ENDPOINT}/{imdb_key}"
        
    except sqlite3.IntegrityError:
        response.sattus = 409
        return ""
    
    
@movies_app.get('/<imdb_key>')
def get_movies(imdb_key):
    c = db.cursor()
    c.execute(
        """
        SELECT   imdb_key, movie_title, movie_year
        FROM     movies
        WHERE imdb_key = ?
        """,
        [imdb_key]

    )

    found = [{"imdbKey": imdb_key,
            "title": title,
            "year": year} 
            for imdb_key, title, year in c]
    if len(found) == 0:
        response.status = 400
    return {"data": found}

