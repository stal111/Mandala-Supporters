import tkinter as tk
import requests
import json

from tkinter import ttk

# load data
patreon_levels = {"Silver Blacksmith": "silver_blacksmith",
                  "Golden Fighter": "golden_fighter",
                  "Arcane Sorcerer": "arcane_sorcerer",
                  "Nebula Club": "nebula_club"}
data = {}


def load_data():
    with open("supporters.json") as file:
        data.update(json.load(file))


def write_data():
    with open("supporters.json", "w") as file:
        jsonObject = json.dumps(data, indent=4)

        file.write(jsonObject)


def get_uuid(name):
    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()

    return request["id"]


def remove_player(name, write=True):
    uuid = get_uuid(name)

    for level in patreon_levels.values():
        levelData = data.get(level)

        if {"id": uuid} in levelData:
            levelData.remove({"id": uuid})

            if write:
                write_data()

            return


def add_player(name, level):
    uuid = get_uuid(name)

    remove_player(name, write=False)

    if level not in patreon_levels.keys():
        return

    data.get(patreon_levels.get(level)).append({"id": uuid})

    write_data()


load_data()

# root window
root = tk.Tk()
root.geometry("300x180")
root.resizable(False, False)
root.title('Mandala Supporters')

# store username and patreon level
local_username = tk.StringVar()
local_patreon_level = tk.StringVar()


def add_clicked():
    """ callback when the add button is clicked
    """

    add_player(local_username.get(), local_patreon_level.get())


def remove_clicked():
    """ callback when the remove button is clicked
    """

    remove_player(local_username.get())


# frame
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill='x', expand=True)

# username
usernameLabel = ttk.Label(frame, text="Username:")
usernameLabel.pack(fill='x', expand=True)

usernameEntry = ttk.Entry(frame, textvariable=local_username, )
usernameEntry.pack(fill='x', expand=True)
usernameEntry.focus()

# patreon level
patreonLevelLabel = ttk.Label(frame, text="Patreon Level:")
patreonLevelLabel.pack(fill='x', expand=True)

patreonLevelCombobox = ttk.Combobox(frame,
                                    textvariable=local_patreon_level,
                                    state="readonly",
                                    values=list(patreon_levels.keys()))

patreonLevelCombobox.pack(fill='x', expand=True)
patreonLevelCombobox.set(list(patreon_levels.keys())[0])

# add supporter button
addButton = ttk.Button(frame, text="Add Supporter", command=add_clicked, state="disabled")
addButton.pack(fill='x', expand=True, pady=10)

# remove supporter Button
removeButton = ttk.Button(frame, text="Remove Supporter", command=remove_clicked, state="disabled")
removeButton.pack(fill='x', expand=True)


def username_change_callback(*args):
    if not local_username.get():
        addButton["state"] = "disabled"
        removeButton["state"] = "disabled"
    else:
        addButton["state"] = "normal"
        removeButton["state"] = "normal"


local_username.trace("w", callback=username_change_callback)

root.mainloop()
