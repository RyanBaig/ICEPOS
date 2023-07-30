import tkinter as tk
from tkinter import ttk


def toggle_fullscreen():
    if window.attributes('-fullscreen'):
        window.attributes('-fullscreen', False)
    elif not window.attributes('-fullscreen'):
        window.attributes('-fullscreen', True)


def toggle_menu():
    if sidebar.winfo_viewable():
        sidebar.grid_remove()
    else:
        sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")


def close_menu():
    sidebar.grid_remove()


# Create the main application window
window = tk.Tk()
window.title("Hamburger Menu Example")
window.geometry("400x300")
window.resizable(False, False)

# Load the PNG icon for the hamburger menu
menu_icon = tk.PhotoImage(file="/media/icons/menu.png")

# Create the hamburger button using the PNG icon
hamburger = tk.Button(window, image=menu_icon, command=toggle_menu, bd=0)
hamburger.grid(row=0, column=0, padx=10, pady=10)

# Create the sidebar (hamburger menu content)
sidebar = tk.Frame(window, bg="lightgray", width=200)
sidebar.grid_remove()  # Initially hidden

# Add some menu items to the sidebar
button = tk.Button(sidebar, text="IDK", command=toggle_fullscreen)
button.grid()
# Add a close button to the sidebar
close_button = tk.Button(sidebar, text="Close", command=close_menu)
close_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Start the Tkinter event loop
window.mainloop()
