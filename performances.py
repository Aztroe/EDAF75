from bottle import Bottle, get, post, run, request, response
import sqlite3

db = sqlite3.connect('movies.sqlite')

performances_endpoint = Bottle()

@performances_endpoint.get('/')
def get_performances():
    c = db.cursor()
    c.execute(
        """
        SELECT   screening_id, start_date, start_time, movie_title, movie_year, theater_name, remaining_seats
        FROM     screening
        """
    )
    response.status = 200
    found = [{"performanceID": screening_id,
              "date": start_date,
              "startTime": start_time,
              "title": movie_title,
              "year": movie_year,
              "theater": theater_name,
              "remainingSeats": remaining_seats} 
              for screening_id, start_date, start_time, movie_title, movie_year, theater_name, remaining_seats in c]
    return {"data": found}

# @movies_endpoint.post('/')
# def create_movie(): # TODO
#     data = request.json()
#     imdb_key = data.get('imdbKey')
#     title = data.get('title')
#     year = data.get('year')

#     c = db.cursor()
#     try:
            
#         c.execute(
#             """
#             SELECT lägg till ....
#             INSERT
#             INTO movies
#             VALUES (?, ?, ?)
#             RETURNING movie
#             """,
#             [imdb_key, title, year]
#         )
#     found = c.fetchone()
#     if not found:
#         response.statue = 400
#         return ""
#     else:
#         response.statue = 201
#         movie = found
#         return f"/movies/{imdb_key}"
    
#     except sqlite.InterruptedError:
#         response.sattus = 409
#         return ""