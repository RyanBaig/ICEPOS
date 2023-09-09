import os
import sqlite3
from tkinter import messagebox
import pickle


def create_db():
        """
        Creates a SQLite database and table if they do not already exist.

        The function first checks if the database file "other\ice-answers.db" exists in the current directory. 
        If the file does not exist, a new SQLite database is created and a connection is established. 
        Otherwise, the function will not create a new database and will proceed with the existing one.

        The function then creates a cursor object from the connection, which will be used to execute SQL commands. 

        Next, the function defines an SQL command to create a table named "answers" with several columns, 
        including shipper_name, shipper_address, shipper_contact, shipment_description, shipment_destination, 
        shipment_service, receiver_name, receiver_address, rec_contact, receiver_zipcode, weight, charges, 
        no_of_pieces, date, and consign_identifier. The table will be created only if it does not already exist.

        The function executes the create table command using the cursor.

        Finally, the changes made to the database are committed, the connection is closed, and a success message is printed.

        Parameters:
        None

        Returns:
        None
        """
        if not os.path.exists("ice-answers.db"):
            # Create a connection to the SQLite database or create a new one if it doesn't exist
            global conn
            conn = sqlite3.connect("ice-answers.db")
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
        """
        Fetches data from an SQLite database table and converts it into a dictionary.

        Returns:
        - ans (dict): A dictionary containing the fetched data from the database. The keys of the dictionary are generated using the combination of the shipper_name and receiver_name values from the database table. The values of the dictionary are dictionaries themselves, containing various attributes related to the shipment.
        """
        # Create a connection to the SQLite database or create a new one if it doesn't exist
        conn = sqlite3.connect("ice-answers.db")

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
        """
        Deletes the SQLite database and table.

        This function establishes a connection to the SQLite database specified by the
        file path "other\\ice-answers.db". It then creates a cursor object to execute
        SQL commands. The function proceeds to drop the table named "answers" from the
        database and commits the changes. Finally, it closes the connection, removes
        the database file, and prints a success message.

        Parameters:
        None

        Returns:
        None
        """
        import os
        # Create a connection to the SQLite database or create a new one if it doesn't exist
        conn = sqlite3.connect("ice-answers.db")

        # Create a cursor object from the connection to execute SQL commands
        cursor = conn.cursor()

        # Now the main part
        cursor.execute('DROP TABLE answers')
        conn.commit()
        conn.close()
        os.remove("ice-answers.db")
        print("SQLite Database and Table Deleted Successfully")


def load_last_consign_key():
    """
    Load the last consign key from the "keys.pkl" file.

    Returns:
        int: The last consign key. If the file is empty or does not exist, returns 0.
    """
    try:
        with open(file="keys.pkl", mode="rb") as file:
            last_key = pickle.load(file)
    except EOFError:
        last_key = 0
    return last_key


def save_last_consign_key(last_key):
        """
        Saves the last consign key to a file.

        Args:
            last_key: The last consign key to be saved.

        Returns:
            None
        """
        with open(file="keys.pkl", mode="wb") as file:
            pickle.dump(last_key, file)

def generate_consign_key():
    """
    Generate a consign key for a new shipment.

    This function retrieves the last consign key from the database using the
    load_last_consign_key function. If the last key is 0, it generates a new
    consign key in the format "ICE-SHIP-0001". Otherwise, it generates a new
    consign key by incrementing the last key and formatting it as
    "ICE-SHIP-{last_key + 1:04}". The new consign key is then saved to the
    database using the save_last_consign_key function. Finally, the generated
    consign key is returned.

    Returns:
        str: The generated consign key.
    """
    last_key = load_last_consign_key()
    if last_key == 0:
        consign_key = "ICE-SHIP-0001"
    else:
        consign_key = f"ICE-SHIP-{last_key + 1:04}"  # Adjust the format as needed
    save_last_consign_key(last_key + 1)
    return consign_key


def display_consign_key():
    """
    Display the last used consign key in a message box.
    
    This function retrieves the latest consign key by calling the `load_last_consign_key` function.
    If the latest key is equal to 0, it is converted to the string "0000".
    The latest key is then displayed in a message box with the message "The latest used consign key is ICE-SHIP-{latest_key}".
    """
    latest_key = load_last_consign_key()
    if latest_key == 0:
        latest_key = "0000"
    messagebox.showinfo("Last Used Consign Key", f"The latest used consign key is ICE-SHIP-{latest_key}.")


def close_connection():
        """
        Closes the connection to the SQLite database.

        :param None:
        :return: None
        """
        # Create a connection to the SQLite database
        conn = sqlite3.connect("ice-answers.db")
        conn.close()



load_last_consign_key()