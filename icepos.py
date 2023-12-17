import tkinter as tk
from tkinter import filedialog
import sqlite3
from PIL import Image, ImageDraw, ImageFont, ImageTk
import screeninfo
import os
from math import pi, cos
import time
import datetime
import requests
import shutil
import subprocess
import pyautogui
from ttkbootstrap.widgets import DateEntry
import threading
from py_functions import (
    close_connection,
    create_db,
    db_to_dict,
    delete_db,
    display_consign_key,
    generate_consign_key,
    create_db_,
    update_icepos,
)
import customtkinter as ctk
from custom_widgets import CustomMessagebox

current_date = datetime.date.today().strftime("%d--%m--%Y")
# Functions:


def check_update():
    time.sleep(1)
    close_connection()

    # Get the current directory of the script
    script_directory = os.path.dirname("C:\\Users\\Hp\\Downloads\\icepos")

    # Move to a different directory to avoid being inside the target directory
    os.chdir(script_directory)

    # Remove the target directory
    target_directory = "./icepos"
    if os.path.exists(target_directory):
        try:
            shutil.rmtree(target_directory)
        except Exception as e:
            print("Error while removing directory:", str(e))
            pass

    # Clone the repository
    update_icepos()

    CustomMessagebox.showinfo("ICEPOS Update", "ICEPOS has been updated.")


def check_update_background():
    """
    Check for updates in the background.

    This function sends a GET request to the specified URL to check for updates.
    If the response status code is 200, it extracts the version number from the JSON
    response and compares it with the current version. If they are not the same, it
    prompts the user with a ctkmessagebox asking if they want to update. If the user
    confirms, it destroys the current window and calls the `execute_check_update`
    function with the new version. If the version numbers are the same, it displays
    a ctkmessagebox informing the user that the application is up to date.

    Parameters:
    None

    Returns:
    None
    """
    CURRENT_VERSION = "v1.4"
    URL = "https://ice-auth.ryanbaig.repl.co/api/check_update"
    r = requests.get(URL)
    if r.status_code == 200:
        VERSION = r.json()["version"]
        if CURRENT_VERSION <= VERSION:
            result = CustomMessagebox.askyesno(
                "Update Needed",
                "An Update has been found, do you want to update ICEPOS right now?",
            )
            if result == "Yes":
                window.destroy()
                check_update()
        else:
            CustomMessagebox.showinfo("Update Information", "ICEPOS is up to date.")


def start_update_check():
    # Run the update check in a separate thread
    update_thread = threading.Thread(target=check_update_background)
    update_thread.start()


def exit_win():
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


def reset():
    """
    Resets the database connection and performs a series of actions to reset the application.

    Args:
        None

    Returns:
        None
    """
    global conn
    conn = sqlite3.connect("ice-answers.db")
    result = CustomMessagebox.askyesno("Confirmation", "Do you want to proceed?")
    if result:
        try:
            conn.close()
        except NameError:
            pass
        except PermissionError:
            window.destroy()
            reset()
        with open(file="keys.pkl", mode="w") as f:
            f.truncate()
        delete_db()
        create_db()
        window.destroy()


def toggle_fullscreen():
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


def get_username():
    """
    Prompts the user to enter their username and saves it to a file.

    Returns:
        None
    """
    dialog = ctk.CTkInputDialog(text="Type Your New Username", title="New Username")
    name = dialog.get_input()
    if name:
        with open(file="username.txt", mode="w") as file:
            file.write(name)
        name_button.configure(text=str(name))




def toggle_menu():
    """
    Toggles the menu by animating the sidebar to slide in or out.

    Parameters:
        None

    Returns:
        None
    """
    current_x = sidebar.winfo_x()
    target_x = -350 if current_x >= 0 else 0
    animate_sidebar(target_x)


def close_menu():
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
    animate_sidebar(target_x)


def animate_sidebar(target_x):
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


# Function to display the selected answer in the Text widget
def display_selected_answer():
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
        refresh_dropdown_and_text()

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
        refresh_dropdown_and_text()
    except KeyError as e:
        print("Error: Shipper-Receiver combination not found in the dictionary.")
        print("Detailed Error:", str(e))
        pass


# Function to update the dropdown and text widget when the Refresh button is clicked
def refresh_dropdown_and_text():
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


def submit():
    """
    Submit the form data to the database, send notifications, and display success message.

    Returns:
        None

    Raises:
        None
    """
    try:
        # Fetch data from the input fields
        ship_name = entry_ship_name.get()
        ship_address = entry_ship_address.get()
        ship_desc = entry_ship_desc.get()
        ship_dest = entry_ship_dest.get()
        ship_serv = entry_ship_serv.get()
        rec_name = entry_rec_name.get()
        rec_address = entry_rec_address.get()
        rec_zipcode = entry_rec_zipcode.get()
        ship_weight = entry_ship_weight.get()
        ship_charges = entry_ship_charges.get()
        no_of_pieces = entry_no_of_pieces.get()
        date = entry_date.entry.get()
        ship_contact = entry_ship_contact.get()
        rec_contact = entry_rec_contact.get()

        # Check if any field is empty
        if any(
            value == ""
            for value in [
                ship_name,
                ship_address,
                ship_desc,
                ship_dest,
                ship_serv,
                rec_name,
                rec_address,
                rec_zipcode,
                ship_weight,
                ship_charges,
                no_of_pieces,
                date,
                ship_contact,
                rec_contact,
            ]
        ):
            CustomMessagebox.showerror("Error", "All fields are required!")
        else:
            # Insert the data into the database
            cursor.execute(
                f"""
                INSERT INTO answers (
                    shipper_name,
                    shipper_address,
                    shipper_contact,
                    shipment_description,
                    shipment_destination,
                    shipment_service,
                    receiver_name,
                    receiver_address,
                    rec_contact,
                    receiver_zipcode,
                    weight,
                    charges,
                    no_of_pieces,
                    date,
                    consign_identifier
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""",
                (
                    ship_name,
                    ship_address,
                    ship_contact,
                    ship_desc,
                    ship_dest,
                    ship_serv,
                    rec_name,
                    rec_address,
                    rec_contact,
                    rec_zipcode,
                    ship_weight,
                    ship_charges,
                    no_of_pieces,
                    date,
                    generate_consign_key(),
                ),
            )

            conn.commit()  # Commit the changes to the database
            # Refresh the dropdown and display the updated data in the Text widget
            refresh_dropdown_and_text()

            def send_notification_and_data(info):
                """
                Send a push notification and data to the specified URL and headers using the Pusher API.

                Args:
                    info (dict): The data payload for the Pusher notification.

                Returns:
                    None

                Raises:
                    None
                """
                import json

                # Define the URL and headers for the Pusher notification
                pusher_url = "https://bd6732cb-f1df-40a9-bf10-1b39a5beeb90.pushnotifications.pusher.com/publish_api/v1/instances/bd6732cb-f1df-40a9-bf10-1b39a5beeb90/publishes"
                pusher_headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer 7A770E61F964B0D25F15CB9470F250EEFF9486967B17E7CF636C25E1ED1E122E",
                }

                # Define the data payload for the Pusher notification
                pusher_data = {
                    "interests": ["hello"],
                    "web": {
                        "notification": {
                            "title": "New Shipment Booked",
                            "body": "Hello, A new Shipment has been booked.",
                            "deep_link": "https://ice-auth.ryanbaig.repl.co/notifications",
                        }
                    },
                }

                # Send the POST request with JSON data for Pusher notification
                pusher_response = requests.post(
                    pusher_url, headers=pusher_headers, json=pusher_data
                )

                # Check the response for Pusher notification
                if pusher_response.status_code == 200:
                    print("Pusher notification sent successfully.")
                else:
                    print(
                        f"Error sending Pusher notification: {pusher_response.status_code} - {pusher_response.text}"
                    )

                # Define the headers with Content-Type as application/json for the second request
                info_headers = {"Content-Type": "application/json"}

                json_info = json.dumps(info)

                # Send an empty JSON object as the request body for the second request
                info_url = "https://ice-auth.ryanbaig.repl.co/notifications"
                info_response = requests.post(
                    info_url, data=json_info, headers=info_headers
                )

                # Check the response for the second request
                if info_response.status_code == 200:
                    print("Notification data sent successfully.")
                    CustomMessagebox.showinfo(
                        "Notification Sent",
                        "Notification with the data has been sent to those concerned.",
                    )
                else:
                    print(
                        f"Error sending notification data: {info_response.status_code} - {info_response.text}"
                    )

            CustomMessagebox.showinfo("Data Submission", "Data Submitted Successfully!")
            data_payload = {
                "ship_name": ship_name,
                "ship_address": ship_address,
                "ship_desc": ship_desc,
                "ship_dest": ship_dest,
                "ship_serv": ship_serv,
                "rec_name": rec_name,
                "rec_address": rec_address,
                "rec_zipcode": rec_zipcode,
                "ship_weight": ship_weight,
                "ship_charges": ship_charges,
                "no_of_pieces": no_of_pieces,
                "date": date,
                "ship_contact": ship_contact,
                "rec_contact": rec_contact,
            }
            thread = threading.Thread(
                target=send_notification_and_data(info=data_payload)
            )
            thread.start()
    except Exception as e:
        print("Error in submit function:", str(e))
        pass


# Function to create a formatted image
def create_formatted_image(
    ship_name,
    ship_address,
    ship_desc,
    ship_dest,
    ship_serv,
    rec_name,
    rec_address,
    rec_zipcode,
    ship_weight,
    ship_charges,
    no_of_pieces,
    date,
    ship_contact,
    rec_contact,
    serial_no,
):
    """
    Create a formatted image using the given information and save it as a PNG file.

    Args:
        ship_name (str): The name of the ship.
        ship_address (str): The address of the ship.
        ship_desc (str): The description of the ship.
        ship_dest (str): The destination of the ship.
        ship_serv (str): The service of the ship.
        rec_name (str): The name of the recipient.
        rec_address (str): The address of the recipient.
        rec_zipcode (str): The zipcode of the recipient.
        ship_weight (str): The weight of the shipment.
        ship_charges (str): The charges for the shipment.
        no_of_pieces (str): The number of pieces in the shipment.
        date (str): The date of the shipment.
        ship_contact (str): The contact information of the ship.
        rec_contact (str): The contact information of the recipient.
        serial_no (str): The serial number of the shipment.

    Returns:
        None
    """
    # Load the background image
    background_img = Image.open("airway_bill_for_printing.png")
    print("Inside create_formatted_image function...")

    # Create a drawing context
    draw = ImageDraw.Draw(background_img)
    print("drawn")
    # Set the font
    font = ImageFont.truetype("arial.ttf", 20)
    print("font")
    # Define the coordinates for placing text on the image
    coordinates = {
        "ship_name": (45, 210),
        "ship_address": (45, 305),
        "ship_desc": (45, 395),
        "ship_dest": (700, 270),
        "ship_serv": (1100, 270),
        "rec_name": (700, 375),
        "rec_address": (700, 470),
        "rec_zipcode": (1052, 580),
        "ship_weight": (45, 595),
        "ship_charges": (470, 595),
        "no_of_pieces": (252, 595),
        "date": (697, 180),
        "ship_contact": (45, 490),
        "rec_contact": (725, 573),
        "serial_no": (1100, 180),
    }

    # Draw the text on the image
    draw.text(coordinates["ship_name"], f"{ship_name}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_address"], f"{ship_address}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_desc"], f"{ship_desc}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_dest"], f"{ship_dest}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_serv"], f"{ship_serv}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["rec_name"], f"{rec_name}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["rec_address"], f"{rec_address}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["rec_zipcode"], f"{rec_zipcode}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_weight"], f"{ship_weight}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_charges"], f"{ship_charges}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["no_of_pieces"], f"{no_of_pieces}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["date"], f"{date}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["ship_contact"], f"{ship_contact}", fill=(0, 0, 0), font=font)
    draw.text(coordinates["rec_contact"], f"{rec_contact}", fill=(0, 0, 0), font=font)
    draw.text(
        coordinates["serial_no"], f"{generate_consign_key()}", fill=(0, 0, 0), font=font
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
        cmd = f'start {path}'
        print(cmd)
        # Open the combined image using the default photo viewer
        os.system(cmd)

        # Wait for the File Explorer window to open
        time.sleep(1)

        # Simulate keypress to trigger print dialog (Ctrl+P)
        pyautogui.hotkey('ctrl', 'p')

        CustomMessagebox.showinfo("Printing", "Formatted image sent to printer.")
    except Exception as e:
        CustomMessagebox.showerror("Printing Error", str(e))


def generate_airway_bill_with_terms_and_conditions():
    """
   This function takes two images, a top image and a bottom image, and combines them into a single image. The combined image
   has the top image in the top-left corner, the bottom image in the bottom-left corner, the top image in the top-right corner,
   and the bottom image in the bottom-right corner. The combined image is then saved in the user's Documents folder under the
   Airway Bills subfolder, using the current date as the filename.

   Args:
       None

   Returns:
       None

   Raises:
       None
   """
    # Open the two images you want to combine
    image_top = Image.open(f"{current_date}.png")
    image_top.thumbnail((1350, 700))
    image_bottom = Image.open("terms_and_conditions.png")
    image_bottom.thumbnail((1350, 700))

    # Get the dimensions of the images
    width, height = 1350, 700

    # Create a new image with the combined width
    combined_image = Image.new("RGB", (width * 2, height * 2), '#ffffff')

    # Paste the top image in the top-left corner
    combined_image.paste(image_top, (0, 0))

    # Paste the bottom image in the bottom-left corner
    combined_image.paste(image_bottom, (0, height))

    # Paste the top image in the top-right corner
    combined_image.paste(image_top, (width, 0))

    # Paste the bottom image in the bottom-right corner
    combined_image.paste(image_bottom, (width, height))

    # Save the combined image with the desired layout
    user = os.path.expanduser('~')
    combined_image.save(f"{user}\\Documents\\Airway Bills\\{current_date}.png")

def print_formatted_image():
    """
    Fetches data from input fields and creates a formatted image.

    Parameters:
        None.

    Returns:
        None.
    """
    # Fetch data from the input fields
    ship_name = entry_ship_name.get()
    ship_address = entry_ship_address.get()
    ship_desc = entry_ship_desc.get()
    ship_dest = entry_ship_dest.get()
    ship_serv = entry_ship_serv.get()
    rec_name = entry_rec_name.get()
    rec_address = entry_rec_address.get()
    rec_zipcode = entry_rec_zipcode.get()
    ship_weight = entry_ship_weight.get()
    ship_charges = entry_ship_charges.get()
    no_of_pieces = entry_no_of_pieces.get()
    date = entry_date.entry.get()
    ship_contact = entry_ship_contact.get()
    rec_contact = entry_rec_contact.get()

    # Create a formatted image
    entries = [
        entry_ship_name,
        entry_ship_address,
        entry_ship_desc,
        entry_ship_dest,
        entry_ship_serv,
        entry_rec_name,
        entry_rec_address,
        entry_rec_zipcode,
        entry_ship_weight,
        entry_ship_charges,
        entry_no_of_pieces,
        entry_ship_contact,
        entry_rec_contact,
    ]
    values = [entry.get() for entry in entries] + [entry_date.entry.get()]
    if any(value == "" for value in values):
        CustomMessagebox.showerror("Error", "All fields are required!")
    else:
        create_formatted_image(
            ship_name,
            ship_address,
            ship_desc,
            ship_dest,
            ship_serv,
            rec_name,
            rec_address,
            rec_zipcode,
            ship_weight,
            ship_charges,
            no_of_pieces,
            date,
            ship_contact,
            rec_contact,
            generate_consign_key(),
        )

        # Print the formatted image
        try:
            generate_airway_bill_with_terms_and_conditions()
            current_date = datetime.date.today().strftime(
                "%d--%m--%Y"
            )
            # Format the date as needed
            print_image(f"{current_date}.png")
            
        except Exception as e:
            CustomMessagebox.showerror("Printing Error", str(e))


# Get the primary monitor information
screen_info = screeninfo.get_monitors()[0]

# Retrieve the monitor width and height
width = screen_info.width
height = screen_info.height

# Add the Theme Settings
ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Create the Tkinter window and set size and icon
window = ctk.CTk()
window.title("ICE AIRWAY BILL")
window.geometry(f"{width}x{height}")
window.iconbitmap("icon.ico")


# Create a Tab Control
tab_control = ctk.CTkTabview(window)

# Create the Submission tab

tab_control.add("Submission")

# Add the Tab Control to the window
tab_control.pack(expand=1, fill="both")

# Create a Canvas widget for the Submission tab
submission_canvas = ctk.CTkCanvas(tab_control.tab("Submission"), width=1350, height=700)
submission_canvas.pack()

# Load the background image for the Submission tab
print("Loading background image...")
background_image_path = "background.png"
print("Background image path:", background_image_path)
try:
    background_image = tk.PhotoImage(file=background_image_path)

    print("Background image loaded successfully.")
    # Create an image item on the canvas with the background image
    submission_canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    print("Background image loaded on canvas successfully.")
except tk.TclError as e:
    print("Error loading background image:", str(e))

# Create the sidebar (hamburger menu content)
sidebar = ctk.CTkFrame(window, width=200)
sidebar.place(x=-300, y=0, relheight=1, anchor=tk.NW)


# Create the hamburger button using the PNG icon
menu_icon = ctk.CTkImage(Image.open("menu.png"))
hamburger = ctk.CTkButton(
    submission_canvas,
    image=menu_icon,
    command=toggle_menu,
    text="",
    height=32,
    width=32,
)
hamburger.place(
    anchor=tk.NW,
)  # Position the hamburger button in the top-left corner

# Label for personal info
personal_info_label = ctk.CTkLabel(
    sidebar, text="Personal Information", font=("Arial", 15)
)
personal_info_label.pack(pady=2)

# Shipper name (1)
entry_ship_name = ctk.CTkEntry(
    tab_control.tab("Submission"), width=550, font=("Arial", 14)
)
entry_ship_name.place(x=45, y=210)

# Shipper Address (2)
entry_ship_address = ctk.StringVar()
entry_ship_address_entry = ctk.CTkEntry(
    tab_control.tab("Submission"),
    width=550,
    font=("Arial", 14),
    textvariable=entry_ship_address,
)
entry_ship_address_entry.place(x=45, y=305)

# Shipment Description (3)
entry_ship_desc = ctk.CTkEntry(
    tab_control.tab("Submission"), width=550, font=("Arial", 14)
)
entry_ship_desc.place(x=45, y=395)

# Shipment Contact # (4)
entry_ship_contact = ctk.CTkEntry(
    tab_control.tab("Submission"), width=240, font=("Arial", 14)
)
entry_ship_contact.place(x=45, y=490)

# Shipment Date (5)
entry_date = DateEntry(tab_control.tab("Submission"), bootstyle="primary", width=37)
entry_date.place(x=697, y=190)

# Shipment Destination (6)
entry_ship_dest = ctk.CTkEntry(
    tab_control.tab("Submission"), width=280, font=("Arial", 14)
)
entry_ship_dest.place(x=700, y=270)

# Shipment Service (7)
entry_ship_serv = ctk.CTkEntry(
    tab_control.tab("Submission"), width=180, font=("Arial", 14)
)
entry_ship_serv.place(x=1100, y=270)

# Receiver Name (8)
entry_rec_name = ctk.CTkEntry(
    tab_control.tab("Submission"), width=550, font=("Arial", 14)
)
entry_rec_name.place(x=700, y=375)

# Receiver Address (9)
entry_rec_address = ctk.StringVar()
entry_rec_address_entry = ctk.CTkEntry(
    tab_control.tab("Submission"),
    width=550,
    font=("Arial", 14),
    textvariable=entry_rec_address,
)
entry_rec_address_entry.place(x=700, y=470)

# Receiver Zipcode (10)
entry_rec_zipcode = ctk.CTkEntry(
    tab_control.tab("Submission"), width=200, font=("Arial", 14)
)
entry_rec_zipcode.place(x=1052, y=580)

# Shipment Weight (11)
entry_ship_weight = ctk.CTkEntry(
    tab_control.tab("Submission"), width=140, font=("Arial", 14)
)
entry_ship_weight.place(x=45, y=595)

# Shipment Charges (12)
entry_ship_charges = ctk.CTkEntry(
    tab_control.tab("Submission"), width=150, font=("Arial", 14)
)
entry_ship_charges.place(x=470, y=595)

# No. of Pieces (13)
entry_no_of_pieces = ctk.CTkEntry(
    tab_control.tab("Submission"), width=130, font=("Arial", 14)
)
entry_no_of_pieces.place(x=260, y=595)

# Consignee Contact (14)
entry_rec_contact = ctk.CTkEntry(
    tab_control.tab("Submission"), width=200, font=("Arial", 14)
)
entry_rec_contact.place(x=725, y=577)

# Create a connection to the SQLite database
conn = sqlite3.connect("ice-answers.db")

# Create a cursor object from the connection
cursor = conn.cursor()

fields = [
    "Shipper Name",
    "Shipper Address",
    "Shipment Description",
    "Shipment Destination",
    "Shipment Service",
    "Receiver Name",
    "Receiver Address",
    "Receiver Zipcode",
    "Shipment Weight",
    "Shipment Charges",
]

# Create Submit Button
submit_button = ctk.CTkButton(
    tab_control.tab("Submission"),
    text="Submit",
    width=10,
    command=lambda: [submit(), refresh_dropdown_and_text()],
)
submit_button.place(x=600, y=600)

# Create Print Button
print_button = ctk.CTkButton(
    tab_control.tab("Submission"),
    text="Print",
    width=10,
    command=lambda: [print_formatted_image(), refresh_dropdown_and_text()],
)
print_button.place(x=710, y=600)

# Bind the close event of the window to close_connection function
window.protocol("WM_DELETE_WINDOW", close_connection)

# Create an Answers tab
tab_control.add("Answers")

# Create a button to input name
name_button = ctk.CTkButton(sidebar, text="Your Username", command=get_username)
name_button.pack(pady=5)

# Label for settings
settings_label = ctk.CTkLabel(sidebar, text="Settings", font=("Arial", 15))
settings_label.pack(pady=2)

saved_username = None
try:
    with open(file="username.txt", mode="r") as file:
        saved_username = file.readline().strip()
except FileNotFoundError:
    pass

if saved_username:
    name_button.configure(text=saved_username)

# Create a new tab in the existing ctk.Notebook widget for the "Tracking" tab

tab_control.add("Tracking")

# Design and add UI elements for tracking
tracking_label = ctk.CTkLabel(
    tab_control.tab("Tracking"), text="Enter Tracking Number:", font=("Arial", 15)
)
tracking_label.pack(pady=10)

tracking_entry = ctk.CTkEntry(
    tab_control.tab("Tracking"), width=300, font=("Arial", 14)
)
tracking_entry.pack(pady=5)

tracking_dropdown = ctk.CTkOptionMenu(
    tab_control.tab("Tracking"), values=["Select the Courier Company", "UPS", "DHL", "FedEx", "TCS", "DPD", "First Flight Courier"], width=300
)
tracking_dropdown.pack(pady=5)


def track_package():
    """
    Retrieves the tracking number from the tracking_entry widget and uses it to make an API request to retrieve tracking information for a package.

    :return: None
    """
    # Retrieve the tracking number from tracking_entry.get()
    courier = tracking_dropdown.get()
    tracking_number = tracking_entry.get()
    url = ""
    if courier == "Select the Courier Company":
        CustomMessagebox.showerror("Error", "Please select a courier company!")
    elif courier == "UPS":
        url = "https://www.ups.com/track?track=yes&trackNums=" + tracking_number
    elif courier == "DHL":
        url = "https://www.dhl.com/pk-en/home/tracking.html?tracking-id=" + tracking_number
    elif courier == "FedEx":
        url = "https://www.fedex.com/fedextrack/?trknbr=" + tracking_number
    elif courier == "TCS":
        url = "https://www.tcsexpress.com/track/" + tracking_number
    elif courier == "DPD":
        url = "https://track.dpd.co.uk"
    elif courier == "First Flight Courier":
        url = "https://firstflightcourier.com.pk/shipment-track.php?FFCODE=" + tracking_number + "&find.x=59&find.y=11"
    import webbrowser
    
    webbrowser.open(url)
    

    


# Function to initiate tracking in a separate thread
def track_package_thread():
    """
    Create and start a new thread to track the package.

    This function creates a new thread using the `threading.Thread` class and sets the target to the `track_package` function. The `track_package` function is responsible for tracking the package and updating its status. Once the thread is created, it is started using the `start` method.

    This function does not have any parameters.

    This function does not return anything.
    """
    tracking_thread = threading.Thread(target=track_package)
    tracking_thread.start()


tracking_button = ctk.CTkButton(
    tab_control.tab("Tracking"), text="Track", width=10, command=track_package_thread
)
tracking_button.pack(pady=5)

# Create a button to toggle fullscreen
fullscreen_button = ctk.CTkButton(
    sidebar, text="Toggle Fullscreen", command=toggle_fullscreen
)
# fullscreen_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
fullscreen_button.pack(side="top", padx=5, pady=5, fill="x")

# Create a button to show last used consign key
last_c_key_button = ctk.CTkButton(
    sidebar, text="Show Last Used Consign Key", command=display_consign_key
)
# last_c_key_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
last_c_key_button.pack(side="top", padx=5, pady=5, fill="x")

# Create a button to check for updates
check_updates_button = ctk.CTkButton(
    sidebar, text="Check For Updates", command=start_update_check
)
# last_c_key_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
check_updates_button.pack(side="top", padx=5, pady=5, fill="x")

# Create a button to reset all data
reset_button = ctk.CTkButton(
    tab_control.tab("Submission"), text="Reset All Data", command=reset
)
reset_button.place(x=650, y=656)

# Create a Text widget to display the answers in the Answers tab
answers_text = ctk.CTkTextbox(tab_control.tab("Answers"), width=600, height=400)
answers_text.pack()
answers_text.configure(state="disabled")  # Set the state to "disabled"

# Create a StringVar to hold the selected answer
selected_answer = ctk.StringVar()

# Create a Combobox for the dropdown
answer_dropdown = ctk.CTkComboBox(
    tab_control.tab("Answers"),
    variable=selected_answer,
    width=500,
    state="readonly",
    values=[""],
)
answer_dropdown.pack()


def refresh_dropdown():
    """
    Refreshes the dropdown menu with the shipper and receiver names from the 'answers' table in the database.

    Parameters:
    None

    Returns:
    None
    """
    cursor.execute("SELECT shipper_name, receiver_name FROM answers")
    shipper_receiver_names = cursor.fetchall()
    answer_dropdown.configure(
        values=[f"{shipper[0]} - {shipper[1]}" for shipper in shipper_receiver_names]
    )


# Function to update the dropdown with shipper-receiver names
def update_dropdown_with_data():
    """
    Update the dropdown widget with data from the database.

    This function retrieves data from the database using the `db_to_dict` function
    and updates the values of the `answer_dropdown` widget. The `answer_dropdown`
    widget is a dropdown widget that allows users to select from a list of options.

    Parameters:
        None

    Returns:
        None
    """
    ans = db_to_dict()
    answer_dropdown.configure(values=list(ans.keys()))
    answer_dropdown.rows = ans


try:
    # Populate the Combobox with the shipper names from the database
    cursor.execute("SELECT shipper_name, receiver_name FROM answers")
except sqlite3.OperationalError as e:
    create_db_()
shipper_receiver_names = cursor.fetchall()
answer_dropdown.configure(
    values=[f"{shipper} - {receiver}" for shipper, receiver in shipper_receiver_names]
)

# Initialize 'rows' attribute for the answer_dropdown
answer_dropdown.rows = {}

# Refresh the dropdown data initially
refresh_dropdown()

# Create a button to display the selected answer
display_button = ctk.CTkButton(
    tab_control.tab("Answers"), text="Display Answer", command=display_selected_answer
)
display_button.pack(padx=10, pady=1)

# Create a button to refresh
refresh_button = ctk.CTkButton(
    tab_control.tab("Answers"), text="Refresh", command=refresh_dropdown_and_text
)
refresh_button.pack()

# Bind the F11 key to toggle fullscreen
window.bind("<F11>", lambda event: toggle_fullscreen())

# Bind the Escape key to toggle fullscreen
window.bind("<Escape>", lambda event: exit_win())

# Retrieve and display the initial data from the table in the Answers tab
cursor.execute("SELECT * FROM answers")
rows = cursor.fetchall()

# Retrieve and display the initial data from the table in the Answers tab
update_dropdown_with_data()

close_button = ctk.CTkButton(sidebar, text="Close", command=close_menu, width=5)
close_button.pack()

# Run the Tkinter event loop
window.mainloop()
