from bottle import Bottle, get, post, run, request, response
import sqlite3

db = sqlite3.connect('movies.sqlite')

movies_endpoint = Bottle()

@movies_endpoint.get('/')
def get_movies():
    c = db.cursor()
    c.execute(
        """
        SELECT   imdb_key, movie_title, movie_year
        FROM     movie
        """
    )
    response.status = 200
    found = [{"imdbKey": imdb_key,
              "title": title,
              "year": year} 
              for imdb_key, title, year in c]
    return {"data": found}

@movies_endpoint.post('/')
def create_movie(): # TODO
    data = request.json()
    imdb_key = data.get('imdbKey')
    title = data.get('title')
    year = data.get('year')

    c = db.cursor()
    c.execute(
        """
        SELECT lägg till ....
        """
    )


#så att värdena returneras rätt och 
# If the IMDB key is already in our database,
# we'll not add anything to the database, 
# return an empty string and the status code 400,
# otherwise we add the movie to our database, return 
# the string /movies/<imdbKey> (i.e., /movies/tt4975722
# for "Moonlight"), and the status code 201.
