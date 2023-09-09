#

[![Release](https://badgers.space/github/release/RyanGamingYT/ICEPOS)](https://github.com/RyanGamingYT/Notepad/releases/tag/v1.2)
![Checks](https://badgers.space//github/checks/RyanGamingYT/ICEPOS)
[![License](https://badgers.space//github/license/RyanGamingYT/ICEPOS)](LICENSE.txt)
![Issues](https://badgers.space//github/open-issues/RyanGamingYT/ICEPOS)
![Languages](https://img.shields.io/github/languages/top/RyanGamingYT/ICEPOS)

#

# ICE POS

ICE POS (Point of Sale) is a Python application created by Me for my father's business. It offers a user-friendly
interface for data submission, retrieval, and printing, along with a custom identifier key for shipment identification.

### Disclaimer

- This code only works on Windows.
- It is designed to only work on a monitor with specific Screen Resolution. Remember to modify it to your needs.

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
- ttkbootstrap: Used for Styling the App and adding the DateEntry.

## Screenshots

#### Submission Tab (Sidebar Closed)

- ![Submission Tab (Sidebar Closed)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Closed).JPG)

#### Submission Tab (Sidebar Open)

- ![Submission Tab (Sidebar Open)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Submission%20Tab%20(Sidebar%20Open).JPG)

#### Answers Tab (No Answer Selected)

- ![Answers Tab (No Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(No%20Answer%20Selected).JPG)

#### Answers Tab (Sample Answer Selected)

- ![Answers Tab (Sample Answer Selected)](https://github.com/RyanGamingYT/ICEPOS/blob/master/media/screenshots/Answers%20Tab%20(Sample%20Answer%20Selected).JPG)

#### Tracking Tab (No Tracking Number Added)

- ![Tracking Tab (No Tracking Number Added)](media/screenshots/Tracking%20Tab%20(No%20Tracking%20Number%20Added).JPG)

#### Tracking Tab (Sample UPS Tracking Number Added)

- ![Tracking Tab (Sample UPS Tracking Number Selected)](media/screenshots/Tracking%20Tab%20(Sample%20UPS%20Tracking%20Number%20Added).JPG)
