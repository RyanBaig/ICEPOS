import os
import sqlite3
from tkinter import messagebox, filedialog, simpledialog

import pickle
import datetime
from PIL import Image, ImageTk, ImageDraw
import requests


def create_db():
    # Create a connection to the SQLite database or create a new one if it doesn't exist
    global conn
    conn = sqlite3.connect(os.path.abspath("other\\ice-answers.db"))
    # Create a cursor object from the connection to execute SQL commands
    global cursor
    cursor = conn.cursor()

    # Define the SQL command to create the table with the specified columns
    create_table_query = """
    CREATE TABLE IF NOT EXISTS answers (
    shipper_name TEXT,
    shipper_address TEXT,
    shipper_contact INTEGER,
    shipment_description TEXT,
    shipment_destination TEXT,
    shipment_service TEXT,
    receiver_name TEXT,
    receiver_address TEXT,
    rec_contact INTEGER,
    receiver_zipcode INTEGER,
    weight TEXT,
    charges TEXT,
    no_of_pieces INTEGER,
    date DATE,
    consign_identifier TEXT PRIMARY KEY
);
    """

    # Execute the create table command
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("SQLite Database and Table Created Successfully.")


def db_to_dict():
    # Create a connection to the SQLite database or create a new one if it doesn't exist
    conn = sqlite3.connect(os.path.abspath("other\\ice-answers.db"))

    # Create a cursor object from the connection to execute SQL commands
    cursor = conn.cursor()

    # Now the main part
    cursor.execute('SELECT * FROM answers')
    rows = cursor.fetchall()

    ans = {}
    for row in rows:
        # Create a key using the combination of shipper_name and receiver_name
        key = f"{row[0]} - {row[6]}"
        ans[key] = {
            "date": row[13],
            "consign_key": row[14],
            "------": "-----",
            "shipper_name": row[0],
            "shipper_address": row[1],
            "shipper_contact": row[2],
            "-----": "-----",
            "receiver_name": row[6],
            "receiver_address": row[7],
            "rec_contact": row[8],
            "receiver_zipcode": row[9],
            "-------": "-----",
            "shipment_description": row[3],
            "shipment_destination": row[4],
            "shipment_service": row[5],
            "no_of_pieces": row[12],
            "shipment_weight": row[10],
            "shipment_charges": row[11]
        }
    return ans


def delete_db():
    import os
    # Create a connection to the SQLite database or create a new one if it doesn't exist
    conn = sqlite3.connect(os.path.abspath("other\\ice-answers.db"))

    # Create a cursor object from the connection to execute SQL commands
    cursor = conn.cursor()

    # Now the main part
    cursor.execute('DROP TABLE answers')
    conn.commit()
    conn.close()
    os.remove(os.path.abspath("other\\ice-answers.db"))
    print("SQLite Database and Table Deleted Successfully")


def load_last_consign_key():
    try:
        with open(file=os.path.abspath("other\\keys.pkl"), mode="rb") as file:
            last_key = pickle.load(file)
    except EOFError:
        last_key = 0
    return last_key


def save_last_consign_key(last_key):
    with open(file=os.path.abspath("other\\keys.pkl"), mode="wb") as file:
        pickle.dump(last_key, file)


def generate_consign_key():
    last_key = load_last_consign_key()
    consign_key = f"ICE-SHIP-{last_key + 1:04}"  # Adjust the format as needed
    save_last_consign_key(last_key + 1)
    return consign_key


def display_consign_key():
    latest_key = load_last_consign_key()
    messagebox.showinfo("Last Used Consign Key", f"The latest used consign key is ICE-SHIP-{latest_key}.")


def close_connection():
    # Create a connection to the SQLite database
    conn = sqlite3.connect(os.path.abspath("other\\ice-answers.db"))
    conn.close()



