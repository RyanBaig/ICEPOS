import datetime
import os
import pickle
import sqlite3
import time
import tkinter as tk
from math import cos, pi
import httpx
import customtkinter as ctk
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import asyncio
from custom_widgets import CustomMessagebox

# Get Current Date & Time
current_date = datetime.datetime.now().strftime("%d-%m-%Y -- %H-%M-%S")

class DB:

    def create_db():
            """
            Creates a SQLite database and table.
            a new SQLite database is created and a connection is established. 
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
            
            

            # Create a connection to the SQLite database or create a new one if it doesn't exist
            global conn
            open(os.path.join(os.path.abspath("."), "assets", "misc", "ice-answers.db"), "w")
            open(os.path.join(os.path.abspath("."), "assets", "misc", "keys.pkl"), "w")
            conn = sqlite3.connect(os.path.join("assets", "misc", "ice-answers.db"))
            # Create a cursor object from the connection to execute SQL commands
            global cursor
            cursor = conn.cursor()

            # Define the SQL command to create the table with the specified columns
            create_table_query = """
                CREATE TABLE IF NOT EXISTS answers (
                shipper_name TEXT,
                shipper_address1 TEXT,
                shipper_address2 TEXT,
                shipper_contact INTEGER,
                shipment_description TEXT,
                shipment_destination TEXT,
                shipment_service TEXT,
                receiver_name TEXT,
                receiver_address1 TEXT,
                receiver_address2 TEXT,
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
            conn = sqlite3.connect(os.path.join("assets", "misc", "ice-answers.db"))

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

        This function establishes a connection to the SQLite database specifiedby the
        file path "other\\os.path.join("assets", "misc", "ice-answers.db")". It then creates a cursor object toexecute
        SQL commands. The function proceeds to drop the table named "answers"from the
        database and commits the changes. Finally, it closes the connection,removes
        the database file, and prints a success message.

        Parameters:
        None

        Returns:
        None
        """

        # Just delete the DB.
        os.remove(os.path.abspath(os.path.join("assets", "misc", "ice-answers.db")))
        print("SQLite Database and Table Deleted Successfully")


    def close_connection():
        """
        Closes the connection to the SQLite database.

        :param None::return: None
                """
        # Create a connection to the SQLite database
        conn = sqlite3.connect(os.path.join("assets", "misc", "ice-answers.db"))
        conn.close()


class Consignment:
    def load_last_consign_key():
        """
        Load the last consign key from the "os.path.join("assets", "misc", "keys.pkl")" file.

        Returns:
            int: The last consign key. If the file is empty or does not exist, returns 0.
        """
        try:
            with open(file=os.path.join("assets", "misc", "keys.pkl"), mode="rb") as file:
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

            with open(file=os.path.join("assets", "misc", "keys.pkl"), mode="wb") as file:
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
        last_key = Consignment.load_last_consign_key()
        if last_key == 0:
            consign_key = "ICE-SHIP-0001"
        else:
            consign_key = f"ICE-SHIP-{last_key + 1:04}"  # Adjust the format as needed
        Consignment.save_last_consign_key(last_key + 1)
        return consign_key


    def display_consign_key():
        """
        Display the last used consign key in a message box.
        
        This function retrieves the latest consign key by calling the `load_last_consign_key` function.
        If the latest key is equal to 0, it is converted to the string "0000".
        The latest key is then displayed in a message box with the message "The latest used consign key is ICE-SHIP-{latest_key}".
        """
        latest_key = Consignment.load_last_consign_key()
        if latest_key == 0:
            latest_key = "0000"
        CustomMessagebox.showinfo("Last Used Consign Key", f"The latest used consign key is ICE-SHIP-{latest_key}.")

class Window:
    def toggle_fullscreen(window):
        """
        Toggle the fullscreen mode of the window.

        This function checks if the window is currently in fullscreen mode using the
        `attributes` method with the argument '-fullscreen'. If the window is already in
        fullscreen mode, it sets the '-fullscreen' attribute to False to toggle it off.
        If the window is not in fullscreen mode, it sets the '-fullscreen' attribute to
        True to toggle it on.

        Parameters:
            None

        Returns:
            None
        """
        if window.attributes("-fullscreen"):
            window.attributes("-fullscreen", False)
        elif not window.attributes("-fullscreen"):
            window.attributes("-fullscreen", True)
    
    
    def exit_win(window):
        """
        Asks the user for confirmation and closes the connection and destroys the window if the user agrees.

        Parameters:
        None

        Returns:
        None
        """
        dialog = CustomMessagebox.askyesno("Confirmation", "Do you want to proceed?")
        if dialog == "Yes":
            window.destroy()
    def get_username(name_button):
        """
        Prompts the user to enter their username and saves it to a file.
        Returns:
            None
        """
        dialog = ctk.CTkInputDialog(text="Type Your New Username", title="New Username")
        name = dialog.get_input()
        if name:
            with open(file="assets\\misc\\username.txt", mode="w") as file:
                file.write(name)
            name_button.configure(text=str(name))

    def character_limit(P):
        if len(P) > 30:
            return False
        else:
            return True

class Menu:
    def toggle_menu(sidebar, window):
        """
        Toggles the menu by animating the sidebar to slide in or out.

        Parameters:
            None

        Returns:
            None
        """
        current_x = sidebar.winfo_x()
        target_x = -350 if current_x >= 0 else 0
        Menu.animate_sidebar(target_x, sidebar, window)


    def close_menu(sidebar, window):
        """
        Closes the menu by setting the animation direction to close and animating the sidebar to the target position.

        Parameters:
            None

        Returns:
            None
        """
        global animation_direction
        animation_direction = 0  # Set direction to close
        target_x = -300  # Target position for closing the sidebar
        Menu.animate_sidebar(target_x, sidebar, window)


    def animate_sidebar(target_x, sidebar, window):
        """
        Animate the sidebar to a target x position.

        Parameters:
            target_x (int): The x position to animate the sidebar to.

        Returns:
            None
        """
        start_x = sidebar.winfo_x()
        distance = target_x - start_x
        duration = 20  # Number of frames for the animation

        for frame in range(1, duration + 1):
            progress = frame / duration
            eased_progress = 0.5 - 0.5 * cos(pi * progress)
            new_x = start_x + distance * eased_progress
            sidebar.place(x=new_x, y=0, relheight=1, anchor=tk.NW)
            window.update()
            time.sleep(0.02)  # Adjust this delay to control the animation speed

class Answer:
    # Function to display the selected answer in the Text widget
    def display_selected_answer(selected_answer, answer_dropdown, answers_text):
        """
        Display the selected answer in the answers_text widget.

        This function updates the dropdown and text with the latest data and then
        fetches the selected answer data from the dropdown.rows dictionary. If the
        selected answer data is not found, the function returns without making any
        changes. Otherwise, it formats and displays all fields of the selected
        answer in the answers_text widget.

        Parameters:
        None

        Returns:
        None
        """
        try:
            # Update the dropdown and text with latest data
            Answer.refresh_dropdown_and_text(answer_dropdown)

            selected_value = selected_answer.get()

            # Fetch the selected answer data from the dropdown.rows dictionary
            ans_dict = answer_dropdown.rows.get(selected_value)

            # If the selected answer data is not found, return without making any changes
            if ans_dict is None:
                return

            answers_text.configure(state="normal")
            answers_text.delete(1.0, ctk.END)

            # Format and display all fields of the selected answer
            for column, value in ans_dict.items():
                answers_text.insert(ctk.END, f"{column}: {value}\n")

            answers_text.configure(state="disabled")
            Answer.refresh_dropdown_and_text(answer_dropdown)
        except KeyError as e:
            print("Error: Shipper-Receiver combination not found in the dictionary.")
            print("Detailed Error:", str(e))
            pass

    async def send_push_message():
        """
        Asynchronous function to send a message using a POST request with JSON data and headers.
        If the response status code is 200, it shows a success message; otherwise, it shows an error message.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 7A770E61F964B0D25F15CB9470F250EEFF9486967B17E7CF636C25E1ED1E122E",
        }

        json_data = {
            "interests": ["ICEPOS"],
            "web": {"notification": {"title": "Shipment Booked!", "body": "Hello Kamran Baig, A new shipment has been booked."}},
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://bd6732cb-f1df-40a9-bf10-1b39a5beeb90.pushnotifications.pusher.com/publish_api/v1/instances/bd6732cb-f1df-40a9-bf10-1b39a5beeb90/publishes",
                headers=headers,
                json=json_data,
            )

            if response.status_code == 200:
                CustomMessagebox.showsuccess(
                    "Message Sent",
                    "A message has been sent to those concerned.",
                )
            else:
                CustomMessagebox.showerror(
                    "Error Sending Message",
                    f"Technical Error: '{response.text}'."
                )

    # Function to update the dropdown and text widget when the Refresh button is clicked
    def refresh_dropdown_and_text(answer_dropdown):
        """
        Refreshes the dropdown menu and text fields with data from the database.
        If there are no records in the database, no changes are made.

        Parameters:
            None

        Returns:
            None
        """
        try:
            # Fetch data from the database
            # Create a connection to the SQLite database or create a new one if it doesn't exist
            global conn
            conn = sqlite3.connect(os.path.join("assets", "misc", "ice-answers.db"))
            # Create a cursor object from the connection to execute SQL commands
            global cursor
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM answers")
            rows = cursor.fetchall()

            # If there are no records in the database, return without making any changes
            if not rows:
                return

            # Update the dropdown with valid shipper-receiver names
            valid_shipper_receiver_names = []
            ans_dict = {}

            for row in rows:
                shipper_name = row[0]
                receiver_name = row[6]
                if shipper_name and receiver_name:
                    shipper_receiver_name = f"{shipper_name} - {receiver_name}"
                    valid_shipper_receiver_names.append(shipper_receiver_name)
                    ans_dict[shipper_receiver_name] = {
                        "Date": row[13],
                        "Consignment Key": row[14],
                        "-----": "-----",
                        "Shipper Name": shipper_name,
                        "Shipper Address": row[1],
                        "Shipper Contact Number": row[2],
                        "------": "-----",
                        "Receiver Name": receiver_name,
                        "Receiver Address": row[7],
                        "Receiver Contact Number": row[8],
                        "Receiver Zipcode": row[9],
                        "-------": "-----",
                        "Shipment Description": row[3],
                        "Shipment Destination": row[4],
                        "Shipment Service": row[5],
                        "Number of Pieces": row[12],
                        "Shipment Weight": row[10],
                        "Shipment Charges": row[11],
                    }

            answer_dropdown["values"] = valid_shipper_receiver_names
            answer_dropdown.rows = ans_dict

        except Exception as error:
            print(f"Error in refresh_dropdown_and_text: {str(error)}")
            pass

    def submit(entries: list, answer_dropdown):
        """
        Submit the form data to the database, send notifications, and display success message.

        Returns:
            None

        Raises:
            None
        """
        print(f"ENTRIES: {entries}")
        # Check if any field is empty
        if any(value == "" for value in entries):
            CustomMessagebox.showerror("Error", "All fields are required!")
        else:
            # Create a connection to the SQLite database or create a new one if it doesn't exist
            global conn
            conn = sqlite3.connect(os.path.join("assets", "misc", "ice-answers.db"))
            # Create a cursor object from the connection to execute SQL commands
            global cursor
            cursor = conn.cursor() 

            # Insert the data into the database
            cursor.execute(
                """
                INSERT INTO answers (
                    shipper_name,
                    shipper_address1,
                    shipper_address2,
                    shipper_contact,
                    shipment_description,
                    shipment_destination,
                    shipment_service,
                    receiver_name,
                    receiver_address1,
                    receiver_address2,
                    rec_contact,
                    receiver_zipcode,
                    weight,
                    charges,
                    no_of_pieces,
                    date,
                    consign_identifier
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (*entries, Consignment.generate_consign_key())
            )

            conn.commit()  # Commit the changes to the database
            # Refresh the dropdown and display the updated data in the Text widget
            Answer.refresh_dropdown_and_text(answer_dropdown)
            CustomMessagebox.showsuccess("Information Submitted", "The Information has been Added to ICEPOS records.")
            asyncio.run(Answer.send_push_message())

    def create_formatted_image(
    ship_name,
    ship_address1,
    ship_address2,
    ship_desc,
    ship_dest,
    ship_serv,
    rec_name,
    rec_address1,
    rec_address2,
    rec_zipcode,
    ship_weight,
    ship_charges,
    no_of_pieces,
    date,
    ship_contact,
    rec_contact,
    serial_no,
):

        # Load the background image

        background_img = Image.open(os.path.join("assets", "images", "airway_bill_for_printing.png"))
        print("Inside create_formatted_image function...")

        # Create a drawing context
        draw = ImageDraw.Draw(background_img)

        # Set the font
        font = ImageFont.truetype(os.path.join("assets", "misc", "Arial.ttf"), 20)

        # Define the coordinates for placing text on the image

        coordinates = {
        "ship_name": (45, 135),
        "ship_address1": (45, 220),
        "ship_address2": (45, 280),
        "ship_desc": (45, 355),
        "ship_contact": (45, 440),
        "date": (620, 140),
        "ship_dest": (620, 230),
        "ship_serv": (975, 230),
        "rec_name": (620, 300),
        "rec_address1": (620, 380),
        "rec_address2": (620, 440),
        "rec_zipcode": (940, 530),
        "ship_weight": (45, 530),
        "ship_charges": (430, 530),
        "no_of_pieces": (230, 530),
        "rec_contact": (650, 530),
        "serial_no": (975, 140)
    }
        # Draw the text on the image
        draw.text(coordinates["ship_name"], f"{ship_name}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_address1"], f"{ship_address1}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_address2"], f"{ship_address2}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_desc"], f"{ship_desc}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_dest"], f"{ship_dest}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_serv"], f"{ship_serv}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["rec_name"], f"{rec_name}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["rec_address1"], f"{rec_address1}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["rec_address2"], f"{rec_address2}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["rec_zipcode"], f"{rec_zipcode}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_weight"], f"{ship_weight}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_charges"], f"{ship_charges}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["no_of_pieces"], f"{no_of_pieces}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["date"], f"{date}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["ship_contact"], f"{ship_contact}", fill=(0, 0, 0), font=font)
        draw.text(coordinates["rec_contact"], f"{rec_contact}", fill=(0, 0, 0), font=font)
        draw.text(
            coordinates["serial_no"], serial_no, fill=(0, 0, 0), font=font
        )
        print("text drawn")
        # Save the formatted image

        background_img.save(f"{current_date}.png")

        # Show a message box indicating the image creation
        CustomMessagebox.showinfo("Image Created", "Formatted image created successfully.")

    # Print function
    def print_image(image_path):
        """
        Print the image located at the given image_path.

        Parameters:
            image_path (str): The path to the image file.

        Returns:
            None
        """
        try:
            path = os.path.abspath(image_path)
            print(path)
            cmd = f'start "{path}"'
            print(cmd)
            # Open the combined image using the default photo viewer
            os.system(cmd)

            # Wait for the File Explorer window to open
            time.sleep(2)

            # Simulate keypress to trigger print dialog (Ctrl+P)
            pyautogui.hotkey('ctrl', 'p')

            CustomMessagebox.showinfo("Printing", "Formatted image sent to printer.")
        except Exception as e:
            CustomMessagebox.showerror("Printing Error", str(e))
