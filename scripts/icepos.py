import tkinter as tk
from tkinter import messagebox, ttk, StringVar, filedialog, simpledialog
import sqlite3
import win32print
import win32ui
import win32con
from PIL import Image, ImageDraw, ImageFont, ImageTk
import screeninfo
import os
import pickle
from math import sin, pi, cos
import time
import datetime
import requests
from py_functions import (
    close_connection, create_db, db_to_dict, delete_db, display_consign_key, generate_consign_key,
    load_last_consign_key, save_last_consign_key, reset, check_update
)
check_update()
# Functions:
def toggle_fullscreen():
    if window.attributes('-fullscreen'):
        window.attributes('-fullscreen', False)
    elif not window.attributes('-fullscreen'):
        window.attributes('-fullscreen', True)


def get_username():
    name = simpledialog.askstring("Username", "Please enter your username")
    if name:
        with open(file=os.path.abspath("other\\username.txt"), mode="w") as file:
            file.write(name)
        name_button.configure(text=name)


def change_profile_pic():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.svg")])
    if file_path:
        rectangular_image = Image.open(file_path)
        resized_image = rectangular_image.resize((120, 120), Image.LANCZOS)

        mask = Image.new("L", (120, 120), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 120, 120), fill=255)

        circular_image = Image.new("RGBA", (120, 120))
        circular_image.paste(resized_image, (0, 0), mask)

        circular_image_tk = ImageTk.PhotoImage(circular_image)

        profile_b.config(image=circular_image_tk)
        profile_b.image = circular_image_tk

        # Save the selected image path to a file
        with open(file=os.path.abspath("other\\selected_image_path.txt"), mode="w") as file:
            file.write(file_path)


def fill_current_date():
    current_date = datetime.date.today().strftime('%d/%m/%Y')  # Format the date as needed
    entry_date.delete(0, tk.END)  # Clear any existing content in the entry
    entry_date.insert(0, current_date)  # Insert the current date into the entry


def toggle_menu():
    current_x = sidebar.winfo_x()
    target_x = -350 if current_x >= 0 else 0
    animate_sidebar(target_x)


def close_menu():
    global animation_direction
    animation_direction = 0  # Set direction to close
    target_x = -300  # Target position for closing the sidebar
    animate_sidebar(target_x)


def animate_sidebar(target_x):
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
        answers_text.delete(1.0, tk.END)

        # Format and display all fields of the selected answer
        for column, value in ans_dict.items():
            answers_text.insert(tk.END, f"{column}: {value}\n")

        answers_text.configure(state="disabled")
        refresh_dropdown_and_text()
    except KeyError as e:
        print("Error: Shipper-Receiver combination not found in the dictionary.")
        print("Detailed Error:", str(e))
        pass


# Function to update the dropdown and text widget when the Refresh button is clicked
def refresh_dropdown_and_text():
    try:
        # Fetch data from the database
        cursor.execute('SELECT * FROM answers')
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
                    "Shipper Name": row[0],
                    "Shipper Address": row[1],
                    "Shipper Contact Number": row[2],
                    "------": "-----",
                    "Receiver Name": row[6],
                    "Receiver Address": row[7],
                    "Receiver Contact Number": row[8],
                    "Receiver Zipcode": row[9],
                    "-------": "-----",
                    "Shipment Description": row[3],
                    "Shipment Destination": row[4],
                    "Shipment Service": row[5],
                    "Number of Pieces": row[12],
                    "Shipment Weight": row[10],
                    "Shipment Charges": row[11]
                }

        answer_dropdown["values"] = valid_shipper_receiver_names
        answer_dropdown.rows = ans_dict

    except Exception as error:
        print(f"Error in refresh_dropdown_and_text: {str(error)}")
        pass


def submit():
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
        date = entry_date.get()
        ship_contact = entry_ship_contact.get()
        rec_contact = entry_rec_contact.get()

        # Check if any field is empty
        if any(value == '' for value in
               [ship_name, ship_address, ship_desc, ship_dest, ship_serv, rec_name, rec_address, rec_zipcode,
                ship_weight, ship_charges, no_of_pieces, date, ship_contact, rec_contact]):
            messagebox.showerror("Error", "All fields are required!")
        else:
            # Insert the data into the database
            cursor.execute(f"""
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
""", (ship_name, ship_address, ship_contact, ship_desc, ship_dest, ship_serv, rec_name, rec_address, rec_contact,
      rec_zipcode, ship_weight, ship_charges, no_of_pieces, date, generate_consign_key()))

            conn.commit()  # Commit the changes to the database
            # Refresh the dropdown and display the updated data in the Text widget
            refresh_dropdown_and_text()
            messagebox.showinfo("Data Submission", "Data Submitted Successfully")
    except Exception as e:
        print("Error in submit function:", str(e))
        pass


# Function to create a formatted image
def create_formatted_image(ship_name, ship_address, ship_desc, ship_dest, ship_serv, rec_name, rec_address, rec_zipcode,
                           ship_weight, ship_charges, no_of_pieces, date, ship_contact, rec_contact, serial_no):
    # Load the background image
    background_img = Image.open(os.path.abspath("media\\images\\airway_bill_for_printing.png"))

    # Create a drawing context
    draw = ImageDraw.Draw(background_img)

    # Set the font
    font = ImageFont.truetype("arial.ttf", 20)

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
        "serial_no": (1100, 180)
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
    draw.text(coordinates["serial_no"], f"{generate_consign_key()}", fill=(0, 0, 0), font=font)

    # Save the formatted image
    background_img.save("formatted_image.png")

    # Show a message box indicating the image creation
    messagebox.showinfo("Image Created", "Formatted image created successfully.")


# Print function
def print_image(image_path):
    try:
        # Open the image using Pillow (Python Imaging Library)
        image = Image.open(image_path)

        # Get the default printer
        printer_name = win32print.GetDefaultPrinter()

        # Create a device context (DC) for the printer
        hdc = win32ui.CreateDC()

        # Set the printer to the default printer
        hdc.CreatePrinterDC(printer_name)

        # Start a print job
        hdc.StartDoc(image_path)

        # Start a page in the print job
        hdc.StartPage()

        # Get the size of the image in pixels
        img_width, img_height = image.size

        dpi = 72
        paper_width = printer_info['pDevMode']['dmPaperWidth'] / 10
        paper_length = printer_info['pDevMode']['dmPaperLength'] / 10

        # Calculate printable width and height in pixels
        printable_width = int(paper_width * dpi / 25.4)
        printable_height = int(paper_length * dpi / 25.4)

        # Calculate the scale factor to fit the image within the printable area
        scale_factor = min(printable_width / img_width, printable_height / img_height)

        # Calculate the position to center the image
        x_center = (printable_width - img_width * scale_factor) / 2
        y_center = (printable_height - img_height * scale_factor) / 2

        # Draw the image on the page
        hdc.StretchBlt((int(x_center), int(y_center), int(img_width * scale_factor), int(img_height * scale_factor)),
                       hdc, (0, 0, img_width, img_height), win32print.SRCCOPY)

        # End the page and the print job
        hdc.EndPage()
        hdc.EndDoc()

        messagebox.showinfo("Printing", "Formatted image sent to printer.")
    except Exception as e:
        messagebox.showerror("Printing Error", str(e))


def print_formatted_image():
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
    date = entry_date.get()
    ship_contact = entry_ship_contact.get()
    rec_contact = entry_rec_contact.get()

    # Create a formatted image
    entries = [entry_ship_name, entry_ship_address, entry_ship_desc, entry_ship_dest, entry_ship_serv,
               entry_rec_name, entry_rec_address, entry_rec_zipcode, entry_ship_weight, entry_ship_charges,
               entry_no_of_pieces,
               entry_date, entry_ship_contact, entry_rec_contact]
    values = [entry.get() for entry in entries]
    if any(value == '' for value in values):
        messagebox.showerror("Error", "All fields are required!")
    else:
        create_formatted_image(ship_name, ship_address, ship_desc, ship_dest, ship_serv, rec_name, rec_address,
                               rec_zipcode, ship_weight, ship_charges, no_of_pieces, date, ship_contact, rec_contact,
                               generate_consign_key())

        # Print the formatted image
        try:
            print_image('formatted_image.png')
        except Exception as e:
            messagebox.showerror("Printing Error", str(e))


# Get the primary monitor information
screen_info = screeninfo.get_monitors()[0]

# Retrieve the monitor width and height
width = screen_info.width
height = screen_info.height

# Create the Tkinter window and set size and icon
window = tk.Tk()
window.title("ICE AIRWAY BILL")
window.geometry(f"{width}x{height}")
window.iconbitmap(os.path.abspath("media/images/icon.ico"))

# Set the style for ttk widgets
style = ttk.Style()

# Use a custom theme to create a more modern look
style.theme_use("clam")  # Options: "clam", "alt", "default", "classic"

# Customize the tttk.Entry widget appearance
style.configure("TEntry", padding=5, font=("Arial", 14))

# Customize the tttk.Button widget appearance
style.configure("TButton", padding=2, font=("Arial", 12))

# Customize the ttk.Combobox widget appearance
style.configure("TCombobox", padding=5, font=("Arial", 14))

# Create a Tab Control
tab_control = ttk.Notebook(window)

# Create the Submission tab
submission_tab = ttk.Frame(tab_control)
tab_control.add(submission_tab, text='Submission')

# Add the Tab Control to the window
tab_control.pack(expand=1, fill="both")

# Create a Canvas widget for the Submission tab
submission_canvas = tk.Canvas(submission_tab, width=1350, height=700)
submission_canvas.pack()

# Load the background image for the Submission tab
background_image = tk.PhotoImage(file=os.path.abspath("media/images/background.png"))

# Place the background image on the Canvas
submission_canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Create the sidebar (hamburger menu content)
sidebar = tk.Frame(window, bg="lightgray", width=200)
sidebar.place(x=-300, y=0, relheight=1, anchor=tk.NW)

# Create the hamburger button using the PNG icon
menu_icon = tk.PhotoImage(file=os.path.abspath("media/images/menu.png"))
hamburger = tk.Button(submission_canvas, image=menu_icon, command=toggle_menu, bd=0)
hamburger.place(x=10, y=10, anchor=tk.NW)  # Position the hamburger button in the top-left corner

personal_info_label = ttk.Label(sidebar, text="Personal Information", font=("Arial", 15))
personal_info_label.pack(pady=5)

# Load the saved image path
saved_image_path = None
try:
    with open(file=os.path.abspath("other\\selected_image_path.txt"), mode="r") as file:
        saved_image_path = file.readline().strip()
except FileNotFoundError:
    pass

# Set the default profile icon or load the saved image
if saved_image_path:
    rectangular_image = Image.open(saved_image_path)
    resized_image = rectangular_image.resize((120, 120), Image.LANCZOS)

    mask = Image.new("L", (120, 120), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 120, 120), fill=255)

    circular_image = Image.new("RGBA", (120, 120))
    circular_image.paste(resized_image, (0, 0), mask)

else:
    circular_image = Image.open(os.path.abspath("media\\images\\default_profile.png"))

circular_image_tk = ImageTk.PhotoImage(circular_image)

# Create the profile button using the loaded/saved image
profile_b = tk.Button(sidebar, image=circular_image_tk, command=change_profile_pic, bd=0, height=120, width=120)
profile_b.image = circular_image_tk  # Store the reference to avoid image garbage collection
profile_b.pack(pady=5)

# Shipper name (1)
entry_ship_name = ttk.Entry(submission_tab, width=55, font=("Arial", 14), style="TEntry")
entry_ship_name.place(x=45, y=210)

# Shipper Address (2)
entry_ship_address = tk.StringVar()
entry_ship_address_entry = ttk.Entry(submission_tab, width=55, font=("Arial", 14), style="TEntry",
                                     textvariable=entry_ship_address)
entry_ship_address_entry.place(x=45, y=305)

# Shipment Description (3)
entry_ship_desc = ttk.Entry(submission_tab, width=55, font=("Arial", 14), style="TEntry")
entry_ship_desc.place(x=45, y=395)

# Shipment Contact # (4)
entry_ship_contact = ttk.Entry(submission_tab, width=24, font=("Arial", 14), style="TEntry")
entry_ship_contact.place(x=45, y=490)

# Shipment Date (5)
entry_date = ttk.Entry(submission_tab, width=23, font=("Arial", 14), style="TEntry")
entry_date.place(x=697, y=180)

fill_c_date = ttk.Button(submission_tab, text="Fill Current Date", command=fill_current_date, style="TButton")
fill_c_date.place(x=760, y=150)

# Shipment Destination (6)
entry_ship_dest = ttk.Entry(submission_tab, width=28, font=("Arial", 14), style="TEntry")
entry_ship_dest.place(x=700, y=270)

# Shipment Service (7)
entry_ship_serv = ttk.Entry(submission_tab, width=18, font=("Arial", 14), style="TEntry")
entry_ship_serv.place(x=1100, y=270)

# Receiver Name (8)
entry_rec_name = ttk.Entry(submission_tab, width=55, font=("Arial", 14), style="TEntry")
entry_rec_name.place(x=700, y=375)

# Receiver Address (9)
entry_rec_address = tk.StringVar()
entry_rec_address_entry = ttk.Entry(submission_tab, width=55, font=("Arial", 14), style="TEntry",
                                    textvariable=entry_rec_address)
entry_rec_address_entry.place(x=700, y=470)

# Receiver Zipcode (10)
entry_rec_zipcode = ttk.Entry(submission_tab, width=20, font=("Arial", 14), style="TEntry")
entry_rec_zipcode.place(x=1052, y=580)

# Shipment Weight (11)
entry_ship_weight = ttk.Entry(submission_tab, width=14, font=("Arial", 14), style="TEntry")
entry_ship_weight.place(x=45, y=595)

# Shipment Charges (12)
entry_ship_charges = ttk.Entry(submission_tab, width=15, font=("Arial", 14), style="TEntry")
entry_ship_charges.place(x=470, y=595)

# No. of Pieces (13)
entry_no_of_pieces = ttk.Entry(submission_tab, width=13, font=("Arial", 14), style="TEntry")
entry_no_of_pieces.place(x=260, y=595)

# Consignee Contact (14)
entry_rec_contact = ttk.Entry(submission_tab, width=20, font=("Arial", 14), style="TEntry")
entry_rec_contact.place(x=725, y=577)

# Create a connection to the SQLite database
conn = sqlite3.connect(os.path.abspath("other\\ice-answers.db"))

# Create a cursor object from the connection
cursor = conn.cursor()

fields = ["Shipper Name", "Shipper Address", "Shipment Description", "Shipment Destination", "Shipment Service",
          "Receiver Name", "Receiver Address", "Receiver Zipcode", "Shipment Weight", "Shipment Charges"]

# Create Submit Button
submit_button = ttk.Button(submission_tab, text="Submit", style="TButton", width=10,
                           command=lambda: [submit(), refresh_dropdown_and_text()])
submit_button.place(x=600, y=600)

# Create Print Button
print_button = ttk.Button(submission_tab, text="Print", width=10, style="TButton",
                          command=lambda: [print_formatted_image(), refresh_dropdown_and_text()])
print_button.place(x=710, y=600)

# Bind the close event of the window to close_connection function
window.protocol("WM_DELETE_WINDOW", close_connection)

# Create an Answers tab
answers_tab = ttk.Frame(tab_control)
tab_control.add(answers_tab, text='Answers')

# Create a button to input name
name_button = ttk.Button(sidebar, text="Your Username", command=get_username)
name_button.pack(pady=5)

# Label for settings
settings_label = ttk.Label(sidebar, text="Settings", font=("Arial", 15))
settings_label.pack(pady=5)

saved_username = None
try:
    with open(file=os.path.abspath("other\\username.txt"), mode="r") as file:
        saved_username = file.readline().strip()
except FileNotFoundError:
    pass

if saved_username:
    name_button.configure(text=saved_username)

# Create a button to toggle fullscreen
fullscreen_button = ttk.Button(sidebar, text="Toggle Fullscreen", command=toggle_fullscreen)
# fullscreen_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
fullscreen_button.pack(side="top", padx=5, pady=5, fill="x")

# Create a button to show last used consign key
last_c_key_button = ttk.Button(sidebar, text="Show Last Used Consign Key", command=display_consign_key)
# last_c_key_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
last_c_key_button.pack(side="top", padx=5, pady=5, fill="x")

# Create a button to reset all data
reset_button = ttk.Button(submission_tab, text="Reset All Data", command=reset)
reset_button.place(x=650, y=656)

# Create a Text widget to display the answers in the Answers tab
answers_text = tk.Text(answers_tab, width=80, height=20)
answers_text.pack()
answers_text.configure(state="disabled")  # Set the state to "disabled"

# Create a StringVar to hold the selected answer
selected_answer = StringVar()

# Create a Combobox for the dropdown
answer_dropdown = ttk.Combobox(answers_tab, style="Custom.TCombobox", textvariable=selected_answer, width=30,
                               state="readonly")
answer_dropdown.pack()


def refresh_dropdown():
    cursor.execute('SELECT shipper_name, receiver_name FROM answers')
    shipper_receiver_names = cursor.fetchall()
    answer_dropdown["values"] = [f"{shipper[0]} - {shipper[1]}" for shipper in shipper_receiver_names]


# Function to update the dropdown with shipper-receiver names
def update_dropdown_with_data():
    ans = db_to_dict()
    answer_dropdown["values"] = list(ans.keys())
    answer_dropdown.rows = ans


# Populate the Combobox with the shipper names from the database
cursor.execute('SELECT shipper_name, receiver_name FROM answers')
shipper_receiver_names = cursor.fetchall()
answer_dropdown["values"] = [f"{shipper} - {receiver}" for shipper, receiver in shipper_receiver_names]

# Initialize 'rows' attribute for the answer_dropdown
answer_dropdown.rows = {}

# Refresh the dropdown data initially
refresh_dropdown()

# Create a button to display the selected answer
display_button = ttk.Button(answers_tab, text="Display Answer", command=display_selected_answer)
display_button.pack(padx=10, pady=1)

# Create a button to refresh
refresh_button = ttk.Button(answers_tab, text="Refresh", command=refresh_dropdown_and_text)
refresh_button.pack()

# Bind the F11 key to toggle fullscreen
window.bind("<F11>", lambda event: toggle_fullscreen())

# Bind the Escape key to toggle fullscreen
window.bind("<Escape>", lambda event: window.destroy())

# Retrieve and display the initial data from the table in the Answers tab
cursor.execute('SELECT * FROM answers')
rows = cursor.fetchall()

# Retrieve and display the initial data from the table in the Answers tab
update_dropdown_with_data()

close_button = ttk.Button(sidebar, text="Close", command=close_menu, width=5)
close_button.pack()

# Run the Tkinter event loop
window.mainloop()
