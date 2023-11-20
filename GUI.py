import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import ctypes
from WADCleaver import *

# Function Definitions:


def select_wad_file():
    wad_file = filedialog.askopenfilename(filetypes=[("WAD Files", "*.wad")])
    wad_entry.delete(0, tk.END)
    wad_entry.insert(0, wad_file)


def select_folder():
    folder = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

# Added by Nepta, callback function
def callback(P):
    if P == "":
        return True
    if len(P) == 1 and P[0] == "-":
        return True
    try:
        int(P)
        return True
    except Exception:
        return False


def generate_wad_folder():
    wad_file = wad_entry.get()
    folder_name = folder_entry.get()
    delim = delim_entry.get()
    token = token_entry.get()

    if wad_file and folder_name:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        params = ["python", "WADCleaver.py", wad_file, folder_name]
        if delim:
            params.extend(["--delim", delim])
        if token:
            params.extend(["--token", token])
        subprocess.call(params)

        # Aquí puedes agregar la lógica para separar los wads en colores

        result_label.config(text="WAD files generated successfully")
    else:
        result_label.config(
            text="Please select a WAD file and type the name of the folder")

ctypes.windll.shcore.SetProcessDpiAwareness(1)
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
window = tk.Tk()
window.title("WADCleaver UI")
window.geometry(f"{int(650 * scaleFactor)}x{int(200 * scaleFactor)}")

# Intro got cut because i switched to using grid.
#intro = tk.Label(text="This is intended to be the GUI for the use of WADCleaver")

# Select the wad file:
wad_label = tk.Label(window, text="Select the WAD file:")
wad_label.grid(row=0, column=0)

wad_entry = tk.Entry(window, width=50)
wad_entry.grid(row=0, column=1)

wad_button = tk.Button(window, text="Select file", command=select_wad_file)
wad_button.grid(row=0, column=2)

folder_label = tk.Label(
    window, text="Select the folder to save the WADs:")
folder_label.grid(row=1, column=0)

folder_entry = tk.Entry(window, width=50)
folder_entry.grid(row=1, column=1)

folder_button = tk.Button(
    window, text="Select directory", command=select_folder)
folder_button.grid(row=1, column=2)

message_label = tk.Label(
    window, text="Reminder: the split WADs will be generated in the location above")
message_label.grid(row=2, column=0, columnspan=3)

# Delimiter added by Nepta
delim_label = tk.Label(window, text="Delimiter")
delim_label.grid(row=3, column=0)

delim_entry = tk.Entry(window, width=50)
delim_entry.grid(row=3, column=1)

# Token added by Nepta
token_label = tk.Label(window, text="Token")
token_label.grid(row=4, column=0)

vcmd = (window.register(callback))
token_entry = tk.Entry(
    window, width=50, validate='all', validatecommand=(vcmd, '%P')
)
token_entry.grid(row=4, column=1)

generate_button = tk.Button(
    window, text="Generate WAD", command=generate_wad_folder)
generate_button.grid(row=5, column=0, columnspan=3)

result_label = tk.Label(window, text="")
result_label.grid(row=6, column=0, columnspan=3)

window.mainloop()