import requests

HOST = "localhost"
PORT = 7007

def post_user(username, full_name, pwd):
    return {
     "username": username,
     "fullName": full_name,
     "pwd": pwd
    }
    

def post_movie(imdb_key, title, year):
    return {
        "imdbKey": imdb_key,
        "title": title,
        "year": year
    }

def post_performance(imdb_key, theater, date, time):
    return {
        "imdbKey": imdb_key,
        "theater": theater,
        "date": date,
        "time": time
    }

def post_ticket(username, pwd, performance_id):
    return {
        "username": username,
        "pwd": pwd,
        "performanceId": performance_id
    }

server_url = f'http://{HOST}:{PORT}/'

r_users = requests.post(server_url + 'users', json=post_user("test_user", "Test Testsson", "psdsksks123"))
print(f"POST /users:  {r_users.status_code}, '{r_users.text}'")

r_movies = requests.post(server_url + 'movies', json=post_movie("tt5537002", "Killers of the Flower Moon", 2023))
print(f"POST /movies: {r_movies.status_code}, '{r_movies.text}'")

r_performances = requests.post(server_url + 'performances', json=post_performance("tt5537002", "Kino", "2024-02-17", "19:30"))
print(f"POST /performances: {r_performances.status_code}, '{r_performances.text}'")
performance_id = r_performances.text.split('/')[1]

r_tickets = requests.post(server_url + 'tickets', json=post_ticket('test_user', 'psdsksks123', performance_id))
print(f"POST /tickets: {r_tickets.status_code}, '{r_tickets.text}'")
