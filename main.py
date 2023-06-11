import os
import datetime as dt
from datetime import timedelta
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from monday_connection import make_folders
from remove_items import deleteFiles



root=ctk.CTk()
root.geometry('720x480')
root.config(padx=50, pady=50, background='light goldenrod')
root.resizable(False, False)

title_label = ctk.CTkLabel(
    root,
    bg_color='light goldenrod',
    font=('Helvetica', 55),
    text_color='black',
    text='JELLYAUTOmate'
).pack()

description = ctk.CTkTextbox(
    root,
    width=460,
    height=100,
    corner_radius=0,
    fg_color='light goldenrod',
    font=('Tahoma', 20),
    text_color='black',
    wrap='word')

description.insert('0.0', 'Tired of making properly-named folders or old files taking up too much disk space? Tire no longer!')
description.configure(state='disabled')
description.pack()


def del_files():
    file_path = filedialog.askdirectory()
    button_frame.destroy()
    instructions = ctk.CTkLabel(
        root,
        text='Files older than X days should be deleted'
    )
    instructions.pack()

    user_input = ctk.CTkEntry(
        root,
        width=100
    )
    user_input.pack()

    del_option1 = ctk.CTkButton(
        root,
        text='Delete Exports',
        command= lambda: deleteFiles(path=file_path, 
                                     date=user_input.get(), 
                                     type='exports')
    ).pack()

    del_option2 = ctk.CTkButton(
        root,
        text='Delete Preedits',
        command=lambda: deleteFiles(path=file_path,
                                    date=user_input.get(),
                                    type='preedits')
    ).pack()



def enter_name():
    button_frame.destroy()
    name_entry = ctk.CTkEntry(root, width=150, placeholder_text='FirstName LastName', fg_color='light goldenrod')
    name_entry.pack(pady=10)
    folder_start = ctk.CTkButton(root, width=50, text="GO", command=lambda: new_item_folder(name_entry.get()))
    folder_start.pack()


def new_item_folder(name):
    file_path = filedialog.askdirectory()
    new_folders = make_folders(file_path, name)
    if new_folders:
        for item in new_folders:
            print(f'The folder {item[0]} was created in {item[1]}')
    else:
        print("No new items were found")
    
'''Make a frame to fit the 2 buttons in the centre'''   
button_frame = ctk.CTkFrame(root, fg_color='light goldenrod')
button_frame.pack()

del_exports = ctk.CTkButton(
    button_frame,
    text='Delete Files',
    command=del_files,
    bg_color='light goldenrod'

)
del_exports.grid(row=0, column=0)

new_folder = ctk.CTkButton(
    button_frame,
    text='Make a New Item Folder',
    command=enter_name,
    bg_color='light goldenrod'
)
new_folder.grid(row=0, column=1)


root.mainloop()
