import os
import sqlite3


def create_db():
    # Create a connection to the SQLite database or create a new one if it doesn't exist
    conn = sqlite3.connect('ice-answers.db')

    # Create a cursor object from the connection to execute SQL commands
    cursor = conn.cursor()

    # Define the SQL command to create the table with the specified columns
    create_table_query = """
    CREATE TABLE IF NOT EXISTS answers (
        shipper_name TEXT,
        shipper_address TEXT,
        shipment_description TEXT,
        shipment_destination TEXT,
        shipment_service TEXT,
        receiver_name TEXT,
        receiver_address TEXT,
        receiver_zipcode INTEGER,
        weight TEXT,
        charges TEXT,
        PRIMARY KEY (shipper_name, receiver_name)
    );
    """

    # Execute the create table command
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("SQLite database and table created successfully.")


def delete_db():
    os.remove("ice-answers.db")
    print("SQLite database and table deleted successfully")


def db_to_dict(fields):
    # Create a connection to the SQLite database or create a new one if it doesn't exist
    conn = sqlite3.connect('ice-answers.db')

    # Create a cursor object from the connection to execute SQL commands
    cursor = conn.cursor()

    # Now the main part
    cursor.execute('SELECT * FROM answers')
    rows = cursor.fetchall()

    ans = {}
    for row in rows:
        # Create a key using the combination of shipper_name and receiver_name
        key = f"{row[0]} - {row[5]}"
        ans[key] = {
            "shipper_name": row[0],
            "shipper_address": row[1],
            "shipment_description": row[2],
            "shipment_destination": row[3],
            "shipment_service": row[4],
            "receiver_name": row[5],
            "receiver_address": row[6],
            "receiver_zipcode": row[7],
            "shipment_weight": row[8],
            "shipment_charges": row[9]
        }
    return ans
