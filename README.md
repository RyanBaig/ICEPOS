# ICE POS

ICE POS (Point of Sale) is a Python application created by Ryan Baig for his father's business. It offers a user-friendly interface for data submission, retrieval, and printing, along with a custom identifier key for shipment identification.

## Installation Instructions

- Clone this repo using the following:
```bash
git clone https://github.com/RyanGamingYT/ICEPOS
```
- Navigate to the project directory using:
```bash
cd ICEPOS
```
- Type `run.bat` or `./run.bat` if you are using Windows Powershell.
- It will automatically install all dependencies (if needed) for the app to work.
- If you want to use it frequently, create a shortcut for the `run.bat` file.

## Features

- [x] Data Submission (Submission Tab)
- [x] Data Retrieval (Answers Tab)
- [x] Printing of Data
- [x] Custom Identifier Key (Consign Key)

## Modules Used

- Tkinter: Used for creating the graphical user interface, including messagebox, ttk, filedialog and simpledialog.
- SQlite3: Used for working with the SQLite database for storing shipping information.
- PyWin32: Utilized for printing functionality using win32print and win32ui.
- Pillow (PIL): Used for image creation, including Image, ImageDraw, and ImageFont.
- Screeninfo: Used for obtaining screen information.
- OS: Used for various operating system-related functionalities.
- Math: Used for math-related operations using sin, cos and pi.
- Time: Used for adding delays between functions.


## Functions

### Stored in [functions.py](scripts/functions.py)

- `close_connection`: Closes the database connection when the main window is closed.
- `create_formatted_image`: Creates a formatted image for printing receipts.
- `display_selected_answer`: Displays selected answers in the Answers Tab.
- `exit_win`: Allows the user to exit the program using the ESC key.
- `print_formatted_image`: Generates and prints a formatted image of the receipt.
- `print_image`: Prints a previously created image.
- `refresh_dropdown`: Refreshes the dropdown in the Answers Tab to check for new submissions.
- `refresh_dropdown_and_text`: Displays answers in the text widget in the Answers Tab.
- `reset`: Clears all submissions by deleting and creating a new SQLite database.
- `submit`: Submits answers to the database.
- `toggle_fullscreen`: Toggles fullscreen mode using F11 key or the button in the top-right corner.
- `update_dropdown_with_data`: Adds support for the dropdown being used more than once.
- `close_menu`: Closes the sidebar/menu and works with toggle_menu.
- `generate_consign_key`: Generates a special key for differentiating shipments.
- `load_last_consign_key`: Loads the last-used consign key.
- `display_consign_key`: Displays the last-used consign key using an information messagebox.
- `toggle_menu`: Toggles the sidebar/menu and uses close_menu.
- `animate_sidebar`: Animates the opening and closing of the sidebar/menu.
- `create_db`: Creates a new database for the reset function.
- `db_To_dict`: Converts database submissions into a dictionary for easy display.
- `delete_db`: Deletes the database for the reset function.

## Screenshots

#### Submission Tab (Sidebar Closed)
![Submission Tab (Sidebar Closed)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Closed).JPG)

#### Submission Tab (Sidebar Open)
![Submission Tab (Sidebar Open)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Open).JPG)

#### Answers Tab (No Answer Selected)
![Answers Tab (No Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(No%20Answer%20Selected).JPG)

#### Answers Tab (Sample Answer Selected)
![Answers Tab (Sample Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(Sample%20Answer%20Selected).JPG)

## License

This Project is Licensed under the [GPL-3.0 License](LICENSE.txt).
