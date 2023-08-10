# ICE POS
## ICE POS (Point of Sale) Type thing I made for my Father's Business
### Features:
- [x] Submission for Data (Submission Tab)
- [x] Retrieval of Data through another Tab in the Tkinter Window (Answers Tab)
- [x] Printing of the Data
- [x] Custom Identifier Key (Consign Key) for shipment identification
### Modules Used:
- [x] Tkinter ([messagebox](https://docs.python.org/3.9/library/tkinter.messagebox.html), [ttk](https://docs.python.org/3.9/library/tkinter.ttk.html), [filedialog](https://docs.python.org/3.9/library/dialog.html), StringVar)
- [x] [Sqlite3](https://docs.python.org/3.9/library/sqlite3.html)
- [x] pywin32 ([win32print](http://timgolden.me.uk/pywin32-docs/win32print.html), [win32ui](http://timgolden.me.uk/pywin32-docs/win32ui.html))
- [x] PIL aka Pillow ([Image](https://pillow.readthedocs.io/en/stable/reference/Image.html), [ImageDraw](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html), [ImageFont](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html))
- [x] Screeninfo (couldn't find the documentation sorry)
- [x] [OS](https://docs.python.org/3/library/os.html)
### Functions: (This will be a very long list)
#### [**icepos.py:**](https://github.com/RyanGamingYT/ICEPOS/blob/master/icepos.py)
- [x] close_connection (To close the connection for the database when the main window is closed Too.)
- [x] create_formatted_image (To create the formatted image for printing.)
- [x] display_selected_answer (To display the answers in the text widget in **Answers Tab**)
- [x] exit_win (To exit the program using ESC key.)
- [x] print_formatted_image (To create and print the formatted image using both the print_image and 
  create_formatted_image functions)
- [x] print_image (To print the previously create image)
- [x] refresh_dropdown (To refresh the dropdown in **Answers Tab** To check for new submissions)
- [x] refresh_dropdown_and_text (To display the answers in the text widget in **Answers Tab**)
- [x] reset (To reset/clear all submissions by deleting and creating a new sqlite database)
- [x] submit (To submit the answers)
- [x] toggle_fullscreen (to Toggle fullscreen through keybind (F11) or the butTon in Top-right corner)
- [x] update_dropdown_with_data (adds support for the dropdown being used more than once)
- [x] close_menu (close the sidebar/menu and works with toggle_menu)
- [x] generate_consign_key (to generate a special key to differentiate between different shipments)
- [x] load_last_consign_key (self-explanatory and works with generate_consign_key)
- [x] display_consign_key (displays the last-used consign key using the information messagebox. Made for the button in sidebar.)
- [x] toggle_menu (to toggle the sidebar/menu and uses close_menu)
#### [**database_functions.py:**](https://github.com/RyanGamingYT/blob/master/database_functions.py)
- [x] create_db (To create the new database for the reset function)
- [x] db_To_dict (converts the submissions stored in the database inTo a dictionary To easily display the information)
- [x] delete_db (To delete the database for the reset function)
### Screenshots:

![Submission Tab (Sidebar Closed)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Closed).JPG)

![Submission Tab (Sidebar Open)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Open).JPG)

![Answers Tab (No Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(No%20Answer%20Selected).JPG)

![Answers Tab (Sample Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(Sample%20Answer%20Selected).JPG)