import os
import datetime as dt
from datetime import timedelta
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from monday_connection import make_folders
from remove_items import deleteFiles


ctk.set_default_color_theme("STYLES/style.json")

root=ctk.CTk()
root.geometry('720x480')
root.config(padx=50, pady=50, background='light goldenrod')
root.resizable(False, False)


title_label = ctk.CTkLabel(
    root,
    bg_color='light goldenrod',
    font=('Helvetica', 60, 'bold'),
    text_color='black',
    text='JELLYAUTOmate'
).pack(pady=(50,0))

description = tk.Text(root, 
                      bg='light goldenrod',
                      fg='black',
                      width=40,
                      height=3,
                      font=('Tahoma', 17),
                      wrap='word',
                      borderwidth=0)

description.tag_configure('center', justify='center')
description.insert('1.0', 'Tired of making properly-named folders or old files\ntaking up too much disk space?\nTire no longer!')
description.tag_add('center', '1.0', 'end')
description.configure(state='disabled')
description.pack(pady=(5, 35))


def del_files():
    file_path = filedialog.askdirectory()
    button_frame.destroy()
    instructions = ctk.CTkLabel(
        root,
        text='Files older than X days should be deleted',
        font=('Helvetica', 15),
        text_color='black',
    )
    instructions.pack(pady=(0, 5))

    user_input = ctk.CTkEntry(
        root,
        width=100
    )
    user_input.pack()

    del_frame = ctk.CTkFrame(root, fg_color='light goldenrod')
    del_frame.pack(pady=10)
    del_option1 = ctk.CTkButton(
        del_frame,
        text='Delete Exports',
        command= lambda: deleteFiles(path=file_path, 
                                     date=user_input.get(), 
                                     type='exports')
    ).grid(row=0, column=0, padx=5, pady=5)

    del_option2 = ctk.CTkButton(
        del_frame,
        text='Delete Preedits',
        command=lambda: deleteFiles(path=file_path,
                                    date=user_input.get(),
                                    type='preedits')
    ).grid(row=0, column=1, padx=5, pady=5)



def enter_name():
    button_frame.destroy()
    name_entry = ctk.CTkEntry(root, width=250, height=35, placeholder_text='FirstName LastName')
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
del_exports.grid(row=0, column=0, padx=5)

new_folder = ctk.CTkButton(
    button_frame,
    text='Make a New Item Folder',
    command=enter_name,
    bg_color='light goldenrod'
)
new_folder.grid(row=0, column=1, padx=5)


root.mainloop()
