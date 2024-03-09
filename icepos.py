import datetime
import os
import sqlite3
import threading
import tkinter as tk

import customtkinter as ctk
import screeninfo
from PIL import Image
from ttkbootstrap.widgets import DateEntry

from custom_widgets import CustomMessagebox
from functions import DB, Answer, Consignment, Menu, Window

# Get Current Date & Time
current_date = datetime.datetime.now().strftime("%d-%m-%Y -- %H-%M-%S")

# Create DB
if not os.path.exists(os.path.abspath(os.path.join("assets", "misc", "ice-answers.db"))):
    DB.create_db()

# Functions:

# Function to create a formatted image





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
    image_bottom = Image.open(os.path.join("assets", "images", "terms_and_conditions.png"))
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
    final_path = os.path.join(user, "Desktop", "Airway-Bills")
    if not os.path.exists(final_path):
        os.makedirs(final_path)

    print(final_path + f"{current_date}.png")

    combined_image.save(os.path.join(final_path, f"{current_date}.png"))

    print("saved final " + final_path)
    os.remove(f"{current_date}.png")

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
    ship_address1 = entry_ship_address1.get()
    ship_address2 = entry_ship_address2.get()
    ship_desc = entry_ship_desc.get()
    ship_dest = entry_ship_dest.get()
    ship_serv = entry_ship_serv.get()
    rec_name = entry_rec_name.get()
    rec_address1 = entry_rec_address1.get()
    rec_address2 = entry_rec_address2.get()
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
        entry_ship_address1,
        entry_ship_address2,
        entry_ship_desc,
        entry_ship_dest,
        entry_ship_serv,
        entry_rec_name,
        entry_rec_address1,
        entry_rec_address2,
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
        Answer.create_formatted_image(
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
            Consignment.generate_consign_key(),
        )

        # Print the formatted image
        try:
            generate_airway_bill_with_terms_and_conditions()
            
            # Format the date as needed
            user = os.path.expanduser('~')
            final_path = os.path.join(user, "Desktop", "Airway-Bills")
            if not os.path.exists(final_path):
                os.makedirs(final_path)
	    
            Answer.print_image(os.path.join(final_path, f"{current_date}.png"))
            
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
window.geometry(f"{width}x{height}"
)



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
background_image_path = os.path.join("assets", "images", "background.png")
print("Background image path:", background_image_path)
try:
    background_image = tk.PhotoImage(file=background_image_path)

    print("Background image loaded successfully.")
    # Create an image item on the canvas with the background image
    submission_canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    # submission_canvas.scale(background_image, 0, 0, 1.5, 1.5)
    print("Background image loaded on canvas successfully.")
except tk.TclError as e:
    print("Error loading background image:", str(e))

# Create the sidebar (hamburger menu content)
sidebar = ctk.CTkFrame(window, width=200)
sidebar.place(x=-300, y=0, relheight=1, anchor=tk.NW)


# Create the hamburger button using the PNG icon
menu_icon = ctk.CTkImage(Image.open(os.path.join("assets", "images", "menu.png")))
hamburger = ctk.CTkButton(
    submission_canvas,
    image=menu_icon,
    text="",
    height=32,
    width=32,
)
hamburger.configure(command=lambda: Menu.toggle_menu(sidebar, window))
hamburger.place(
    anchor=tk.NW,
)  
# Position the hamburger button in the top-left corner

# Label for personal info
personal_info_label = ctk.CTkLabel(
    sidebar, text="Personal Information", font=("Arial", 15)
)
personal_info_label.pack(pady=2)



# ------ INPUTS ---------

# Shipper name (1)
entry_ship_name = ctk.CTkEntry(
    tab_control.tab("Submission"), width=540, font=("Arial", 14)
)
entry_ship_name.place(x=45, y=135)

# Shipper Address 1 (2)
entry_ship_address1 = ctk.StringVar()
entry_ship_address_entry1 = ctk.CTkEntry(
    tab_control.tab("Submission"),
    width=550,
    font=("Arial", 14),
    textvariable=entry_ship_address1,
    validate="key",
    validatecommand=(window.register(Window.character_limit), '%P')
)

entry_ship_address_entry1.place(x=45, y=220)

# Shipper Address 2 (3)
entry_ship_address2 = ctk.StringVar()
entry_ship_address_entry2 = ctk.CTkEntry(
    tab_control.tab("Submission"),
    width=550,
    font=("Arial", 14),
    textvariable=entry_ship_address2,
    validate="key",
    validatecommand=(window.register(Window.character_limit), '%P')
)

entry_ship_address_entry2.place(x=45, y=280)

# Shipment Description (4)
entry_ship_desc = ctk.CTkEntry(
    tab_control.tab("Submission"), width=550, font=("Arial", 14)
)
entry_ship_desc.place(x=45, y=355)

# Shipment Contact # (5)
entry_ship_contact = ctk.CTkEntry(
    tab_control.tab("Submission"), width=240, font=("Arial", 14)
)
entry_ship_contact.place(x=45, y=440)

# Shipment Date (6)
entry_date = DateEntry(tab_control.tab("Submission"), bootstyle="primary", width=37)
entry_date.place(x=620, y=140)

# Shipment Destination (7)
entry_ship_dest = ctk.CTkEntry(
    tab_control.tab("Submission"), width=280, font=("Arial", 14)
)
entry_ship_dest.place(x=620, y=230)

# Shipment Service (8)
entry_ship_serv = ctk.CTkEntry(
    tab_control.tab("Submission"), width=180, font=("Arial", 14)
)
entry_ship_serv.place(x=970, y=230)

# Receiver Name (9)
entry_rec_name = ctk.CTkEntry(
    tab_control.tab("Submission"), width=550, font=("Arial", 14)
)
entry_rec_name.place(x=620, y=300)

# Receiver Address 1 (10)
entry_rec_address1 = ctk.StringVar()
entry_rec_address_entry1 = ctk.CTkEntry(
    tab_control.tab("Submission"),
    width=550,
    font=("Arial", 14),
    textvariable=entry_rec_address1,
    validate="key",
    validatecommand=(window.register(Window.character_limit), '%P')
)
# Use trace to call character_limit whenever the text changes

entry_rec_address_entry1.place(x=620, y=380)

# Receiver Address 2 (11)
entry_rec_address2 = ctk.StringVar()
entry_rec_address_entry = ctk.CTkEntry(
    tab_control.tab("Submission"),
    width=550,
    font=("Arial", 14),
    textvariable=entry_rec_address2,
    validate="key",
    validatecommand=(window.register(Window.character_limit), '%P')
)
entry_rec_address_entry.place(x=620, y=440)

# Receiver Zipcode (12)
entry_rec_zipcode = ctk.CTkEntry(
    tab_control.tab("Submission"), width=200, font=("Arial", 14)
)
entry_rec_zipcode.place(x=940, y=530)

# Shipment Weight (13)
entry_ship_weight = ctk.CTkEntry(
    tab_control.tab("Submission"), width=140, font=("Arial", 14)
)
entry_ship_weight.place(x=45, y=530)

# Shipment Charges (14)
entry_ship_charges = ctk.CTkEntry(
    tab_control.tab("Submission"), width=150, font=("Arial", 14)
)
entry_ship_charges.place(x=430, y=530)

# No. of Pieces (15)
entry_no_of_pieces = ctk.CTkEntry(
    tab_control.tab("Submission"), width=130, font=("Arial", 14)
)
entry_no_of_pieces.place(x=230, y=530)

# Consignee Contact (16)
entry_rec_contact = ctk.CTkEntry(
    tab_control.tab("Submission"), width=200, font=("Arial", 14)
)
entry_rec_contact.place(x=650, y=530)

# Create a connection to the SQLite database
conn = sqlite3.connect(os.path.join("assets", "misc", "ice-answers.db"))

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
    command=lambda: [
        Answer.submit(entries=[
                entry_ship_name.get(),
                 entry_ship_address1.get(),
                  entry_ship_address2.get(),
                   entry_ship_desc.get(),
                    entry_ship_dest.get(),
                     entry_ship_serv.get(),
                      entry_rec_name.get(),
                       entry_rec_address1.get(),
                        entry_rec_address2.get(),
                         entry_rec_zipcode.get(),
                          entry_ship_weight.get(),
                           entry_ship_charges.get(),
                            entry_no_of_pieces.get(),
                             entry_date.entry.get(),
                              entry_ship_contact.get(),
                               entry_rec_contact.get()],
                               answer_dropdown=answer_dropdown
                                ),
                                Answer.refresh_dropdown_and_text(answer_dropdown)
                                ],
)
submit_button.place(x=600, y=600)

# Create Print Button
print_button = ctk.CTkButton(
    tab_control.tab("Submission"),
    text="Print",
    width=10,
    command=lambda: [print_formatted_image(), Answer.refresh_dropdown_and_text(answer_dropdown)],
)
print_button.place(x=710, y=600)

# Bind the close event of the window to close_connection function
window.protocol("WM_DELETE_WINDOW", DB.close_connection)

# Create an Answers tab
tab_control.add("Answers")

# Create a button to input name
name_button = ctk.CTkButton(sidebar, text="Your Username")
name_button.configure(command=lambda: Window.get_username(name_button))
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
    sidebar, text="Toggle Fullscreen", command=lambda: Window.toggle_fullscreen(window)
)

# fullscreen_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
fullscreen_button.pack(side="top", padx=5, pady=5, fill="x")

# Create a button to show last used consign key
last_c_key_button = ctk.CTkButton(
    sidebar, text="Show Last Used Consign Key", command=Consignment.display_consign_key
)
# last_c_key_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
last_c_key_button.pack(side="top", padx=5, pady=5, fill="x")

# last_c_key_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")




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
    ans = DB.db_to_dict()
    answer_dropdown.configure(values=list(ans.keys()))
    answer_dropdown.rows = ans


try:
    # Populate the Combobox with the shipper names from the database
    cursor.execute("SELECT shipper_name, receiver_name FROM answers")
except sqlite3.OperationalError:
    DB.create_db()
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
    tab_control.tab("Answers"), text="Display Answer")
display_button.configure(command=lambda: Answer.display_selected_answer(selected_answer, answer_dropdown, answers_text))
display_button.pack(padx=10, pady=1)

# Create a button to refresh
refresh_button = ctk.CTkButton(
    tab_control.tab("Answers"), text="Refresh")
refresh_button.configure(command=Answer.refresh_dropdown_and_text(answer_dropdown))
refresh_button.pack()

# Bind the F11 key to toggle fullscreen
window.bind("<F11>", lambda event: Window.toggle_fullscreen(window))


# Bind the Escape key to toggle fullscreen
window.bind("<Escape>", lambda event: Window.exit_win(window))

# Retrieve and display the initial data from the table in the Answers tab
cursor.execute("SELECT * FROM answers")
rows = cursor.fetchall()

# Retrieve and display the initial data from the table in the Answers tab
update_dropdown_with_data()

close_button = ctk.CTkButton(sidebar, text="Close", width=5)
close_button.configure(command=lambda: Menu.close_menu(sidebar, window))
close_button.pack()

# Run the Tkinter event loop
window.mainloop()
