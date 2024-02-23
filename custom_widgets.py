import os

from CTkMessagebox import CTkMessagebox


class CustomMessagebox:
    def showinfo(title, message):
        icon_path = os.path.join("assets", "icons", "info.png")
        CTkMessagebox(title=title, message=message, sound=True, icon=icon_path)

    def showerror(title, message):
        icon_path = os.path.join("assets", "icons", "cancel.png")
        CTkMessagebox(title=title, message=message, icon=icon_path, sound=True)

    def askyesno(title, message):
            # get yes/no answers
            icon_path = os.path.join("assets", "icons", "question.png")
            msg = CTkMessagebox(title=title, message=message,
                                icon=icon_path, option_1="Cancel", option_2="No", option_3="Yes",
                                 sound=True)
            response = msg.get()
            return response

    def showsuccess(title, message):
        icon_path = os.path.join("assets", "icons", "check.png")
        CTkMessagebox(title=title, message=message, icon=icon_path, sound=True)
