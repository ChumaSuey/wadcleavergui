import tkinter as tk
from tkinter import filedialog
import subprocess
import os
from WADCleaver import *

#Function Definitions:

def select_wad_file():
    wad_file = filedialog.askopenfilename(filetypes=[("WAD Files", "*.wad")])
    wad_entry.delete(0, tk.END)
    wad_entry.insert(0, wad_file)

def select_folder():
    folder = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

def generate_wad_folder():
    wad_file = wad_entry.get()
    folder_name = folder_entry.get()

    if wad_file and folder_name:
        if not os.path.exists(folder_name):
         os.makedirs(folder_name)
         subprocess.call(["python", "Wadcleaver.py", wad_file, folder_name]) # Añadi un "-o" como parametro pero no sirvio
            # Aquí puedes agregar la lógica para separar los wads en colores

        result_label.config(text="Carpeta generada con éxito")
    else:
        result_label.config(text="Por favor, selecciona un archivo .wad y proporciona un nombre de carpeta")


window = tk.Tk()
intro = tk.Label(text="This is intended to be the GUI for the use of WADCleaver")
window.title("WADCleaver UI")
intro.pack()
window.geometry("400x200")

wad_label = tk.Label(window, text="Select the wad file") #Selecciona el archivo .wad:
wad_label.pack()

wad_entry = tk.Entry(window, width=50)
wad_entry.pack()

wad_button = tk.Button(window, text="Select file", command=select_wad_file)
wad_button.pack()

folder_label = tk.Label(window, text="Select the folder to save the separated WADs")
folder_label.pack()

folder_entry = tk.Entry(window, width=50)
folder_entry.pack()


folder_button = tk.Button(window, text="Select directory", command=select_folder)
folder_button.pack()

message_label = tk.Label(window, text="Reminder: the split WADs will be generated in the location above")
message_label.pack()

generate_button = tk.Button(window, text="Generate folder", command=generate_wad_folder)
generate_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()



