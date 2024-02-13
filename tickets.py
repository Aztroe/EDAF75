from bottle import Bottle, get, post, run, request, response
import sqlite3
from users import hash as user_pwd_hash

db = sqlite3.connect('movies.sqlite')

tickets_app = Bottle()
TICKETS_ENDPOINT = '/tickets'

@tickets_app.post('/')
def create_ticket():
    data = request.json
    username = data.get('username')
    password = data.get('pwd')
    password = user_pwd_hash(password)
    performance_id = data.get('performanceId')

    c = db.cursor()

    # OK if:
    # there is such a performance, 
    c.execute(
        """
        SELECT  performance_id
        FROM    performances
        WHERE   performance_id = ?
        """,
        [performance_id]
    )
    if c.fetchone() is None:
        response.status = 400 
        return "Error" # TODO, make less vague?

    # there is a user with the given username and password, 
    c.execute(
        """
        SELECT  username, pass_wrd
        FROM    customers
        WHERE   username = ? AND pass_wrd = ?
        """,
        [username, password]
    )
    if c.fetchone() is None:
        response.status = 401
        return "Wrong user credentials"

    # and there are still free seats
    c.execute(
        """
        SELECT  iif(ticket_id IS NULL, 0, count()) AS count, capacity
        FROM    performances
                JOIN      theaters  USING (theater_name)
                LEFT JOIN tickets   USING (performance_id)
        WHERE   performance_id = ?
        """,
        [performance_id]
    )

    count, capacity = c.fetchone()
    remaining_seats = capacity - count
    if remaining_seats == 0:
        response.status = 400
        return "No tickets left"
    elif remaining_seats < 0:
        response.status = 400
        return "Error" # TODO, make less vague?

    try:  
        c.execute(
            """
            INSERT
            INTO        tickets(customer_username, performance_id)
            VALUES      (?, ?)
            RETURNING   ticket_id
            """,
            [username, performance_id]
        )
        ticket_id, = c.fetchone()
        db.commit()
        response.status = 201
        return f"{TICKETS_ENDPOINT}/{ticket_id}"
    except sqlite3.DatabaseError:
        response.status = 400
        return "Error" # TODO, make less vague?

    # except sqlite3.IntegrityError:
    #     response.status = 400
    #     return "Error" # TODO, make less vague?
    # except sqlite3.OperationalError:
    #     response.status = 400
    #     return "Error" # TODO, make less vague?