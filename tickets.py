# from bottle import Bottle, get, post, run, request, response
# import sqlite3

# db = sqlite3.connect('movies.sqlite')

# movies_endpoint = Bottle()

# @movies_endpoint.get('/')
# def get_movies():
#     c = db.cursor()
#     c.execute(
#         """
#         SELECT   imdb_key, movie_title, movie_year
#         FROM     movie
#         """
#     )
#     response.status = 200
#     found = [{"imdbKey": imdb_key,
#               "title": title,
#               "year": year} 
#               for imdb_key, title, year in c]
#     return {"data": found}

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