from models import Animal
from models import Location
from models import Customer
import sqlite3
import json

def get_all_animals():
    # Open a connection to the database
    # These three lines are how we talk to the database
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        # db cursor is just letting us make a sql query
        # Telling the db what info to get and what table to get it from
        # """ allows for multi line strings
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            c.password customer_password
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        # Grabs everything that matches the SELECT query above
        # gets the result
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            # using backet notation to grab the info off of the 'row'
            # this has to match the select above
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])

            location = Location(row['location_id'], row['location_name'], row['location_address'])
            animal.location = location.__dict__

            customer = Customer(row['id'], row['customer_name'], row['customer_address'], row['customer_email'], row['customer_password'])
            animal.customer = customer.__dict__

            # adding animal dictionary to the animal list (like a push) above which is equal to an empty array []
            animals.append(animal.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)

def get_single_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        # we define data and that is why we pass data in our animal = Animal section below
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        # sets up init and passes in all the paramaters
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return json.dumps(animal.__dict__)


def create_animal(new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        # SQL query
        # Insert the new animal into the database, this will match my python db
        # new_animal[] section needs to match the object in React
        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return json.dumps(new_animal)

def delete_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        # You should be able to explain what SQL statement is needed to remove a row from a database table.
        # You should be able to implement and explain how to use a SQL parameter to remove a single row from a database table.
        # You should be able to implement a Python function in a module whose reposibility is to remove a single row from a database table.
        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()
        # You should be able to identify a SQL query that is changing the state of a row in a database table.
        # You should be able to implement multiple SQL parameters in a query.
        # You should be able to implement a SQL statement that updates the database with the state that was sent by the client in an HTTP request.
        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_animals_by_location(location_id):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, ( location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'] , row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)


def get_animals_by_status(status):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'] , row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)