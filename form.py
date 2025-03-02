import toml
from tkinter import *
import subprocess

# Define the default settings
default_settings = {
    "server": {
        "ip": "157.138.166.198",
        "port": 3000
    },
    "paths": {
        "base": "C:/Users/iit_c/Desktop/scanner_socket",
        "folder": "test_folder",
    }
}


# Function to save the settings to the TOML file and run main.py
def save_settings():
    settings = {
        "server": {
            "ip": ip_entry.get(),
            "port": int(port_entry.get())
        },
        "paths": {
            "base": base_entry.get(),
            "folder": folder_entry.get(),
        }
    }
    with open("settings.toml", "w") as f:
        toml.dump(settings, f)
    print("Settings saved to settings.toml")
    root.destroy()

    subprocess.run(["python", "main.py"])


root = Tk()
root.title("Artec EVA remote scanning")
root.geometry("350x165")

# Create the form fields
Label(root, text="Server IP:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
ip_entry = Entry(root, width=25)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Server Port:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
port_entry = Entry(root, width=25)
port_entry.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Base Path:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
base_entry = Entry(root, width=25)
base_entry.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Folder:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
folder_entry = Entry(root, width=25)
folder_entry.grid(row=3, column=1, padx=10, pady=5)


# Populate the form with the default settings
ip_entry.insert(0, default_settings["server"]["ip"])
port_entry.insert(0, str(default_settings["server"]["port"]))
base_entry.insert(0, default_settings["paths"]["base"])
folder_entry.insert(0, default_settings["paths"]["folder"])

save_button = Button(root, text="Save and Run", command=save_settings)
save_button.grid(row=5, column=0, columnspan=2, pady=10)

root.eval('tk::PlaceWindow . center')

root.mainloop()
