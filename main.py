import os
import datetime as dt
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from monday_connection import make_folders
from remove_items import deleteFiles


# os.getcwd() - get current directory
# os.chdir() - change directory to specified path
# os.listdir() - list all files and subdirectories
# os.remove(file) - removes file in current directory
# os.path.getctime(file dir) - returns time of creation of specified file

root=tk.Tk()
root.geometry('1280x720')
root.config(pady=50)
options_label = tk.Label(
    text='Choose an option'
)
options_label.pack()


def del_files():
    file_path = filedialog.askdirectory()
    options_label.destroy()
    del_exports.destroy()
    new_folder.destroy()
    instructions = tk.Label(
        root,
        text='Files older than X days should be deleted'
    )
    instructions.pack()

    user_input = tk.Entry(
        root,
        width=100
    )
    user_input.pack()

    del_option1 = tk.Button(
        text='Delete Exports',
        command= lambda: deleteFiles(path=file_path, 
                                     date=user_input.get(), 
                                     type='exports')
    ).pack()

    del_option2 = tk.Button(
        text='Delete Preedits',
        command=lambda: deleteFiles(path=file_path,
                                    date=user_input.get(),
                                    type='preedits')
    ).pack()


def new_item_folder():
    options_label.destroy()
    del_exports.destroy()
    file_path = filedialog.askdirectory()
    new_folders = make_folders(file_path)
    if new_folders:
        for item in new_folders:
            print(f'The folder {item[0]} was created in {item[1]}')
    else:
        print("No new items were found")
    

del_exports = tk.Button(
    text='Delete Files',
    command=del_files
)
del_exports.pack()

new_folder = tk.Button(
    text='Make a New Item Folder',
    command=new_item_folder
)
new_folder.pack()


root.mainloop()
