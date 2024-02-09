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

server_url = f'http://{HOST}:{PORT}/'

r = requests.post(server_url + 'users', json=post_user("test_user", "Test Testsson", "psdsksks123"))
print(r.status_code)