# ICE POS
## ICE POS (Point of Sale) Type thing I made for my Father's Business
### Features:
- [x] Submission for Data (Submission Tab)
- [x] Retrieval of Data through another Tab in the Tkinter Window (Answers Tab)
- [x] Printing of the Data
### Modules Used:
- [x] Tkinter ([messagebox](https://docs.python.org/3.9/library/tkinter.messagebox.html), [ttk](https://docs.python.org/3.9/library/tkinter.ttk.html), [filedialog](https://docs.python.org/3.9/library/dialog.html), StringVar)
- [x] [Sqlite3](https://docs.python.org/3.9/library/sqlite3.html)
- [x] pywin32 ([win32print](http://timgolden.me.uk/pywin32-docs/win32print.html), [win32ui](http://timgolden.me.uk/pywin32-docs/win32ui.html))
- [x] PIL aka Pillow ([Image](https://pillow.readthedocs.io/en/stable/reference/Image.html), [ImageDraw](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html), [ImageFont](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html))
- [x] Screeninfo (couldn't find the documentation sorry)
- [x] [Os](https://docs.python.org/3/library/os.html)
### Functions: (This will be a very long list)
#### [**icepos.py:**](https://github.com/RyanGamingYT/ICEPOS/master/icepos.py)
- [x] close_connection (To close the connection for the database when the main window is closed Too.)
- [x] create_formatted_image (To create the formatted image for printing.)
- [x] display_selected_answer (To display the answers in the text widget in **Answers Tab**)
- [x] exit (To exit the program using ESC key.)
- [x] print_formatted_image (To create and print the formatted image using both the print_image and 
  create_formatted_image functions)
- [x] print_image (To print the previously create image)
- [x] refresh_dropdown (To refresh the dropdown in **Answers Tab** To check for new submissions)
- [x] refresh_dropdown_and_text (To display the answers in the text widget in **Answers Tab**)
- [x] reset (To reset/clear all submissions by deleting and creating a new sqlite database)
- [x] submit (To submit the answers)
- [x] Toggle_fullscreen (To Toggle fullscreen through keybind (F11) or the butTon in Top-right corner)
- [x] update_dropdown_with_data (adds support for the dropdown being used more than once)
#### [**database_functions.py:**](https://github.com/RyanGamingYT/master/database_functions.py)
- [x] create_db (To create the new database for the reset function)
- [x] db_To_dict (converts the submissions stored in the database inTo a dictionary To easily display the information)
- [x] delete_db (To delete the database for the reset function)
