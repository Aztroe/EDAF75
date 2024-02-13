from bottle import Bottle, get, post, run, request, response
import sqlite3

db = sqlite3.connect('movies.sqlite')

performances_app = Bottle()
PERFORMANCES_ENDPOINT = '/performances'

@performances_app.get('/')
def get_performances():
    c = db.cursor()

    c.execute(
        """
        WITH ticket_counts AS (
            SELECT      performance_id, iif(ticket_id IS NULL, 0 ,count()) AS ticket_count
            FROM        performances
                        LEFT JOIN tickets USING (performance_id)
            GROUP BY    performance_id
        )
        
        SELECT      performance_id, start_date, start_time, movie_title, movie_year, theater_name, capacity - ticket_count
        FROM        performances
                    JOIN  theaters       USING (theater_name)
                    JOIN  ticket_counts  USING (performance_id)
        """
    )

    found = [{"performanceId": performance_id,
              "date": start_date,
              "startTime": start_time,
              "title": movie_title,
              "year": movie_year,
              "theater": theater_name,
              "remainingSeats": remaining_seats} 
              for performance_id, start_date, start_time, movie_title, movie_year, theater_name, remaining_seats in c]
    response.status = 200
    return {"data": found}

@performances_app.post('/')
def add_performance():
    data = request.json
    imdb_key = data.get('imdbKey')
    theater_name = data.get('theater')
    date = data.get('date')
    time = data.get('time')

    c = db.cursor()
    try:
        c.execute( # "COUNT(*)" eller bara "*" ?
            """
            SELECT theater_name
            FROM theaters
            WHERE theater_name = ?
            """,
            [theater_name]
        )
        theater_cols = c.fetchone()

        c.execute(
            """
            SELECT movie_title, movie_year
            FROM movies
            WHERE imdb_key = ?
            """,
            [imdb_key]
        )

        movie_cols = c.fetchone()

        if movie_cols is None or theater_cols is None:
            response.status = 400
            return "No such movie or theater"
        else:
            movie_title, movie_year = movie_cols
            c.execute( # kolla performance vad som ska in, inte rätt nu
                """
                INSERT
                INTO performances(start_date, start_time, theater_name, movie_title, movie_year)
                VALUES (?, ?, ?, ?, ?)
                RETURNING performance_id
                """,
                [date, time, theater_name, movie_title, movie_year]
            )
            performance_id = c.fetchone()[0]
            db.commit()
            response.status = 201
            return f"{PERFORMANCES_ENDPOINT}/{performance_id}"
            
    except Exception as e:
        print(f"An error occured: {e}")
        response.status = 500
        return "internal Server Error"