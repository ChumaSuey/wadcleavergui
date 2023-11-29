import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import ctypes
from WADCleaver import *

# Function Definitions:

#This function will select the map file through the browser
def select_wad_file():
    wad_file = filedialog.askopenfilename(filetypes=[("WAD Files", "*.wad")])
    wad_entry.delete(0, tk.END)
    wad_entry.insert(0, wad_file)

# This function will select the folder the directory where the chopped WAD is selected.
# Note that this function will "Select" where the files will be downloaded so a final section
# Must named where folder should be saved.
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

# The key function: generate WAD folder
# This function will generate the folder with the chopped WADs with the extra info (delim and/or token)
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

     #This will just generate the WAD file or the error message.

        result_label.config(text="WAD files generated successfully")
    else:
        result_label.config(
            text="Please select a wad file and type the name of the folder")

#In this section the graphical / tkinter part of the project begins
ctypes.windll.shcore.SetProcessDpiAwareness(1)
scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
window = tk.Tk()
intro = tk.Label(
    text="This is intended to be the GUI for the use of WADCleaver")
window.title("WADCleaver UI")
intro.pack()
window.geometry(f"{int(600 * scaleFactor)}x{int(300 * scaleFactor)}")
# Suggested by Pixelkiri,  geometry and ctypes for enhanced UI, with scalefactor for better window resolution.

# The next are just the labels and entries for the script to work.
wad_label = tk.Label(window, text="Select the wad file")
wad_label.pack()

wad_entry = tk.Entry(window, width=50)
wad_entry.pack()

wad_button = tk.Button(window, text="Select file", command=select_wad_file)
wad_button.pack()

folder_label = tk.Label(
    window, text="Select the folder to save the separated WADs")
folder_label.pack()

folder_entry = tk.Entry(window, width=50)
folder_entry.pack()

folder_button = tk.Button(
    window, text="Select directory", command=select_folder)
folder_button.pack()

message_label = tk.Label(
    window, text="Reminder: the split WADs will be generated in the location above")
message_label.pack()

#Delimiter added by Nepta
delim_label = tk.Label(window, text="Delimiter")
delim_label.pack()

delim_entry = tk.Entry(window, width=50)
delim_entry.pack()

#Token added by Nepta
token_label = tk.Label(window, text="Token")
token_label.pack()
vcmd = (window.register(callback))
token_entry = tk.Entry(
    window, width=50, validate='all', validatecommand=(vcmd, '%P')
)
token_entry.pack()



generate_button = tk.Button(
    window, text="Generate WAD", command=generate_wad_folder)
generate_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
