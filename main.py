import os
import datetime as dt
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog

# os.getcwd() - get current directory
# os.chdir() - change directory to specified path
# os.listdir() - list all files and subdirectories
# os.remove(file) - removes file in current directory

filename = 'C://Users/Stoyan/CodingProjects/Jelly/jelly.txt'
creation_date = os.path.getctime(filename)

root=tk.Tk()
root.geometry('1280x720')
# root.withdraw()
options_label = tk.Label(
    text='Choose an option'
)
options_label.pack()


def del_files():
    file_path = filedialog.askdirectory()
    options_label.destroy()
    del_exports.destroy()
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


    def init_delete():
        all_files = os.listdir(file_path)
        for file in all_files:
            creation_date = os.path.getctime(f'{file_path}/{file}')
            readable_date = dt.datetime.fromtimestamp(creation_date).date()
            if readable_date >= dt.date.today() - timedelta(days=int(user_input.get())):
                print('yes')
                os.remove(f'{file_path}/{file}')

    delete = tk.Button(
        text='Delete',
        command=init_delete
    ).pack()


    



del_exports = tk.Button(
    text='Delete Exported Files',
    command=del_files
)
del_exports.pack()





root.mainloop()