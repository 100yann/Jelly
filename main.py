import os
import datetime as dt
from datetime import timedelta
import tkinter as tk
from tkinter import filedialog

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
        root_dir = os.listdir(file_path)
        for num, season in enumerate(root_dir):
            if f'SEASON_{num}' in root_dir or f'season_{num}' in root_dir or f'Season_{num}' in root_dir:
                all_episodes = os.listdir(file_path+f'/SEASON_{num}')
                for episode in all_episodes:
                    if "CREXXX" in episode:
                        pass
                    else:
                        try:
                            end_dir = file_path + f'/SEASON_{num}' + f'/{episode}/1_EXPORTS/1_MASTERS/3_FACEBOOK'
                            all_exports = os.listdir(end_dir)
                            for export in all_exports:
                                creation_date = os.path.getctime(f'{end_dir}/{export}')
                                readable_date = dt.datetime.fromtimestamp(creation_date).date()
                                if readable_date <= dt.date.today() - timedelta(days=int(user_input.get())):
                                    try:
                                        os.remove(f'{end_dir}/{export}')
                                    except PermissionError:
                                        pass
                        except FileNotFoundError:
                            pass

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
