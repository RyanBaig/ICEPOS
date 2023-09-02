# [![Release](https://badgers.space//github/release/RyanGamingYT/ICEPOS)](https://github.com/RyanGamingYT/Notepad/releases/tag/v1.1) ![Checks](https://badgers.space//github/checks/RyanGamingYT/ICEPOS) [![License](https://badgers.space//github/license/RyanGamingYT/ICEPOS)](LICENSE.txt) ![Issues](https://badgers.space//github/open-issues/RyanGamingYT/ICEPOS) ![Maintainability](https://badgen.net/codeclimate/maintainability/RyanGamingYT/ICEPOS) ![Languages](https://img.shields.io/github/languages/top/RyanGamingYT/ICEPOS) ![Coverage](https://img.shields.io/codeclimate/coverage/RyanGamingYT/ICEPOS?style=flat&logo=codeclimate)

# ICE POS

ICE POS (Point of Sale) is a Python application created by Me for my father's business. It offers a user-friendly 
interface for data submission, retrieval, and printing, along with a custom identifier key for shipment identification.

### Disclaimer:
- This code only works on Windows.
- It is designed to only work on a monitor with specific Screen Resolution. Remember to modify it to your needs.

## Installation Instructions:
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
- If you want to use it frequently then create a shortcut ([ICEPOS.ink](ICE%20POS.lnk)) for the `run.bat` file. 

## Features

- [x] Data Submission (Submission Tab)
- [x] Data Retrieval (Answers Tab)
- [x] Printing of Data
- [x] Custom Identifier Key (Consign Key)

## Modules Used

- Tkinter: Used for creating the graphical user interface, including messagebox, ttk, and filedialog.
- Sqlite3: Used for working with the SQLite database.
- Pillow (PIL): Used for image creation, including Image, ImageDraw, and ImageFont.
- Pickle: Used for serializing and deserializing data, but in this application to store consignment keys. 
- Math: used for Math-related operations including Pi values, Sin, Con operations.
- Time: used to add delays.
- Datetime: used for retreiving date.
- Requests: used for checking for any updates for ICEPOS.
- Subprocess: used in Updating process by cloning the repository using [Git](https://www.git-scm.com).
- Shutil: Used to delete pre-existing installations of ICEPOS to make room for the New Update.
- Stat: used for manipulating folder permissions.
- Screeninfo: Used for obtaining screen information.
- OS: Used for various operating system-related functionalities including printing, finding absolute path of files, etc.

## Functions

### [icepos.py](scripts/icepos.py)


- `create_formatted_image`: Creates a formatted image for printing receipts.
- `display_selected_answer`: Displays selected answers in the Answers Tab.
- `exit_win`: Allows the user to exit the program using the ESC key.
- `print_formatted_image`: Generates and prints a formatted image of the receipt.
- `print_image`: Prints a previously created image.
- `refresh_dropdown`: Refreshes the dropdown in the Answers Tab to check for new submissions.
- `refresh_dropdown_and_text`: Displays answers in the text widget in the Answers Tab.
- `submit`: Submits answers to the database.
- `toggle_fullscreen`: Toggles fullscreen mode using F11 key or the button in the top-right corner.
- `update_dropdown_with_data`: Adds support for the dropdown being used more than once.
- `close_menu`: Closes the sidebar/menu and works with toggle_menu.
- `toggle_menu`: Toggles the sidebar/menu and uses close_menu.
- `on_rm_error`: Used for manipulating .git folder's properties while updating._
- `git_clone_with_progress`: Clones the repository for updating and shows live progress using messagebox. Uses `on_rm_error` function.
- `check_update`: Checks if any updation is needed.
- `execute_check_update`: Starts the updating process. Uses `git_clone_with_progress` function.


### [py_functions.py](scripts/py_functions.py)


- `reset`: Clears all submissions by deleting and creating a new SQLite database.
- `save_last_consign_key`: Saves the consign key in [keys.pkl](other/keys.pkl).
- `generate_consign_key`: Generates a special key for differentiating shipments.
- `load_last_consign_key`: Loads the last-used consign key.
- `display_consign_key`: Displays the last-used consign key using an information messagebox.
- `close_connection`: Closes the database connection when the main window is closed.
- `create_db`: Creates a new database for the reset function.
- `db_To_dict`: Converts database submissions into a dictionary for easy display.
- `delete_db`: Deletes the database for the reset function.


### [run.py](scripts/run.py)


- `check_packages`: Checks if any packages need to be installed (from [requirements.txt](other/requirements.txt)) when the 
  program is [run](run.bat). "

## Screenshots
#### Submission Tab (Sidebar Closed)
- ![Submission Tab (Sidebar Closed)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Closed).JPG)
#### Submission Tab (Sidebar Open)
- ![Submission Tab (Sidebar Open)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Open).JPG)
#### Answers Tab (No Answer Selected)
- ![Answers Tab (No Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(No%20Answer%20Selected).JPG)
#### Answers Tab (Sample Answer Selected)
- ![Answers Tab (Sample Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(Sample%20Answer%20Selected).JPG)

