from CTkMessagebox import CTkMessagebox


class CustomMessagebox:
    def showinfo(title, message):
        CTkMessagebox(title=title, message=message, sound=True, icon="assets\\icons\\info.png")

    def showerror(title, message):
        CTkMessagebox(title=title, message=message, icon="assets\\icons\\cancel.png", sound=True)

    def askyesno(title, message):
            # get yes/no answers
            msg = CTkMessagebox(title=title, message=message,
                                icon="assets\\icons\\question.png", option_1="Cancel", option_2="No", option_3="Yes",
                                 sound=True)
            response = msg.get()
            return response

    def showsuccess(title, message):
        CTkMessagebox(title=title, message=message, icon="assets\\icons\\check.png", sound=True)
