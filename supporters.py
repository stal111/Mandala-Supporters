import tkinter as tk
import requests
import json

from tkinter import ttk
from tkinter.messagebox import showinfo

# root window
root = tk.Tk()
root.geometry("300x150")
root.resizable(False, False)
root.title('Mandala Supporters')

# store username and patreon level
username = tk.StringVar()
patreonLevel = tk.StringVar()


class Popup:
    def __init__(self, master=None, title: str = "Popup", message: str = ""):
        if master is None:
            # If the caller didn't give us a master, use the default one instead
            master = tk._get_default_root()

        # Create a toplevel widget
        self.root = tk.Toplevel(master)
        # A min size so the window doesn't start to look too bad
        self.root.minsize(200, 60)
        # Stop the user from resizing the window
        self.root.resizable(False, False)
        # If the user presses the `X` in the titlebar of the window call
        # self.destroy()
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        # Set the title of the popup window
        self.root.title(title)

        # Calculate the needed width/height
        width = max(map(len, message.split("\n")))
        height = message.count("\n") + 1
        # Create the text widget
        self.text = tk.Text(self.root, bg="#f0f0ed", height=height,
                            width=width, highlightthickness=0, bd=0)
        # Add the text to the widget
        self.text.insert("end", message)
        # Make sure the user can't edit the message
        self.text.config(state="disabled")
        self.text.pack()

        # Make sure the user isn't able to spawn new popups while this is
        # still alive
        self.root.grab_set()
        # Stop code execution in the function that called us
        self.root.mainloop()

    def destroy(self) -> None:
        # Stop the `.mainloop()` that's inside this class
        self.root.quit()
        # Destroy the window
        self.root.destroy()


def add_clicked():
    """ callback when the add button clicked
    """

    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username.get()}").json()

    value = {"id": request["id"], "level": patreonLevel.get()}

    msg = f'You entered email: {username.get()} and password: {patreonLevel.get()}'

    Popup(master=root, title="Json code", message="#" + username.get() + "\n" + json.dumps(value))


# frame
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill='x', expand=True)

# username
usernameLabel = ttk.Label(frame, text="Username:")
usernameLabel.pack(fill='x', expand=True)

usernameEntry = ttk.Entry(frame, textvariable=username, )
usernameEntry.pack(fill='x', expand=True)
usernameEntry.focus()

# patreon level
patreonLevelLabel = ttk.Label(frame, text="Patreon Level:")
patreonLevelLabel.pack(fill='x', expand=True)

patreonLevelCombobox = ttk.Combobox(frame,
                                    textvariable=patreonLevel,
                                    state="readonly",
                                    values=("Silver Blacksmith", "Golden Fighter", "Arcane Sorcerer", "Nebula Club"))

patreonLevelCombobox.pack(fill='x', expand=True)
patreonLevelCombobox.set("Silver Blacksmith")

# add supporter button
addButton = ttk.Button(frame, text="Add Supporter", command=add_clicked, state="disabled")
addButton.pack(fill='x', expand=True, pady=10)


def username_change_callback(*args):
    if not username.get():
        addButton["state"] = "disabled"
    else:
        addButton["state"] = "normal"


username.trace("w", callback=username_change_callback)

root.mainloop()

