from CTkMessagebox import CTkMessagebox

class CustomMessagebox:
    def showinfo(title, message):
        CTkMessagebox(title=title, message=message, sound=True, icon="icons\info.png", fade_in_duration=5)

    def showerror(title, message):
        CTkMessagebox(title=title, message=message, icon="icons\cancel.png", sound=True, fade_in_duration=5)

    def askyesno(title, message):
            # get yes/no answers
            msg = CTkMessagebox(title=title, message=message,
                                icon="icons\question.png", option_1="Cancel", option_2="No", option_3="Yes",
                                 sound=True, fade_in_duration=5)
            response = msg.get()
            return response


