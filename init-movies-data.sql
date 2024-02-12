PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theater;
DROP TABLE IF EXISTS screening;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS customer;

PRAGMA foreign_keys=ON;

CREATE TABLE theater (
    theater_name    TEXT,
    capacity        INTEGER,
    PRIMARY KEY  (theater_name)
);

CREATE TABLE screening (
    screening_id    TEXT,
    start_date      DATE,
    start_time      TIME,
    theater_name    TEXT,
    movie_title     TEXT,
    movie_year      INTEGER,
    remaining_seats INTEGER,
    FOREIGN KEY  (theater_name) REFERENCES theater(theater_name),
    FOREIGN KEY  (movie_title, movie_year)  REFERENCES movie(movie_title, movie_year),
    PRIMARY KEY  (screening_id)
    -- PRIMARY KEY  (theater_name, movie_title, movie_year, start_date, start_time)
);

CREATE TABLE movie (
    movie_title     TEXT,
    movie_year      INTEGER,
    imdb_key        TEXT,
    -- run_time        TIME,
    PRIMARY KEY  (movie_title, movie_year)
);

CREATE TABLE ticket (
    ticket_id           TEXT DEFAULT (lower(hex(randomblob(16)))),
    customer_username   TEXT,
    theater_name        TEXT,
    movie_title         TEXT,
    movie_year          INTEGER,
    start_date          DATE,
    start_time          TIME,
    PRIMARY KEY  (ticket_id),
    FOREIGN KEY  (customer_username)       REFERENCES customer(username),
    FOREIGN KEY  (theater_name, movie_title, movie_year, start_date, start_time) REFERENCES screening(theater_name, movie_title, movie_year, start_date, start_time)
);

CREATE TABLE customer (
    username    TEXT,
    full_name   TEXT,
    pass_wrd    TEXT,
    PRIMARY KEY  (username)
);

------------------------------------------------

DELETE FROM theater;
DELETE FROM screening;
DELETE FROM movie;
DELETE FROM ticket;
DELETE FROM customer;

INSERT
INTO   theater(theater_name, capacity)
VALUES ('Filmstaden', 175),
       ('Kino',       50),
       ('SF Bio',     100);

INSERT
INTO   movie(movie_title, movie_year, imdb_key, run_time)
VALUES ('Titanic',        1997, 'tt0120338', '03:14'),
       ('The Rise and Fall of Scooby Doo', 2002, 'tt0267913', '01:29'),
       ('The Rise and Fall of Scooby Doo', 2019, 'tt2294449', '01:52'),
       ('Interstellar', 2014, 'tt0816692', '02:49'),
       ('Inception', 2010, 'tt1375666', '02:28'),
       ('The Grand Budapest Hotel', 2014, 'tt2278388', '01:39');

INSERT
INTO   customer(username, full_name, pass_wrd)
VALUES ('vitooo', 'Victor Truong',  '1234'),
       ('freddy', 'Fredrik Orheim', '2345'),
       ('Bona',   'Jona Waldfogel', '3456'),
       ('john_doe', 'John Doe', 'password123'),
       ('jane_smith', 'Jane Smith', 'securepassword'),
       ('alex_brown', 'Alex Brown', 'anotherpass');

INSERT
INTO   screening(start_date, start_time, theater_name, movie_title, movie_year)
VALUES  ('2024-02-10', '14:00', 'Filmstaden', 'Titanic', 1997),
        ('2024-02-10', '18:00', 'Filmstaden', 'Titanic', 1997),
        ('2024-02-11', '20:00', 'Kino', 'The Rise and Fall of Scooby Doo', 2002),
        ('2024-02-12', '16:00', 'SF Bio', 'The Rise and Fall of Scooby Doo', 2019),
        ('2024-02-13', '19:00', 'Filmstaden', 'Interstellar', 2014),
        ('2024-02-14', '21:00', 'Kino', 'Inception', 2010),
        ('2024-02-15', '17:00', 'SF Bio', 'The Grand Budapest Hotel', 2014),
        ('2024-02-16', '14:00', 'Filmstaden', 'Interstellar', 2014),
        ('2024-02-17', '20:00', 'Kino', 'Inception', 2010),
        ('2024-02-18', '18:00', 'SF Bio', 'The Rise and Fall of Scooby Doo', 2019),
        ('2024-03-08', '18:00', 'Filmstaden', 'Titanic', 1997),
        ('2024-03-09', '19:30', 'Filmstaden', 'The Rise and Fall of Scooby Doo', 2002),
        ('2024-03-09', '19:30', 'Kino',       'Titanic', 1997),
        ('2024-03-10', '20:00', 'SF Bio',     'The Rise and Fall of Scooby Doo', 2019);


-- INSERT
-- INTO   ticket(customer_username, theater_name, movie_title, movie_year, start_date, start_time)
-- VALUES ('vitooo', 'Filmstaden', '', 0, '', 'YYYY-MM-DD', 'HH:MM'),
--        ('freddy', 'Filmstaden', '', 0, '', 'YYYY-MM-DD', 'HH:MM'),
--        ('Bona',   'Filmstaden', '', 0, '', 'YYYY-MM-DD', 'HH:MM'),

