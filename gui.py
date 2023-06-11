import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from monday_connection import make_folders
from remove_items import deleteFiles



class Program:
    ctk.set_default_color_theme("STYLES/style.json")
    
    def __init__(self, parent):
        self.parent = parent
        title_label = ctk.CTkLabel(
            self.parent,
            bg_color='light goldenrod',
            font=('Helvetica', 60, 'bold'),
            text_color='black',
            text='JELLYAUTOmate'
        ).pack(pady=(50,0))

        description = ctk.CTkTextbox(self.parent, 
                            fg_color='light goldenrod',
                            width=425,
                            height=80,
                            font=('Tahoma', 17),
                            text_color='black',
                            wrap='word',
                            border_width=0)

        description.tag_config('center', justify='center')
        description.insert('1.0', 'Tired of making properly-named folders or old files\ntaking up too much disk space?\nTire no longer!')
        description.tag_add('center', '1.0', 'end')
        description.configure(state='disabled')
        description.pack(pady=(5, 25))
        self.start_buttons()


    def start_buttons(self):  
        '''Make a frame to fit the 2 buttons in the centre''' 
        self.button_frame = ctk.CTkFrame(self.parent, fg_color='light goldenrod')
        self.button_frame.pack()

        del_exports = ctk.CTkButton(
            self.button_frame,
            text='Delete Files',
            command=self.del_files,
            bg_color='light goldenrod'

        )
        del_exports.grid(row=0, column=0, padx=5)

        new_folder = ctk.CTkButton(
            self.button_frame,
            text='Make a New Item Folder',
            command=self.enter_name,
            bg_color='light goldenrod'
        )
        new_folder.grid(row=0, column=1, padx=5)

    def del_files(self):
        file_path = filedialog.askdirectory()
        self.button_frame.destroy()
        self.instructions = ctk.CTkLabel(
            self.parent,
            text='Files older than X days should be deleted',
            font=('Helvetica', 15),
            text_color='black',
        )
        self.instructions.pack(pady=(0, 5))

        self.user_input = ctk.CTkEntry(
            self.parent,
            width=100
        )
        self.user_input.pack()

        self.del_frame = ctk.CTkFrame(self.parent, fg_color='light goldenrod')
        self.del_frame.pack(pady=10)
        del_option1 = ctk.CTkButton(
            self.del_frame,
            text='Delete Exports',
            command= lambda: deleteFiles(path=file_path, 
                                        date=self.user_input.get(), 
                                        type='exports')
        ).grid(row=0, column=0, padx=5, pady=5)

        del_option2 = ctk.CTkButton(
            self.del_frame,
            text='Delete Preedits',
            command=lambda: deleteFiles(path=file_path,
                                        date=self.user_input.get(),
                                        type='preedits')
        ).grid(row=0, column=1, padx=5, pady=5)
        self.home_button = ctk.CTkButton(self.parent,
                                        text='BACK',
                                        width=40,
                                        command= lambda:self.homescreen(
                                                        self.instructions,
                                                        self.user_input,
                                                        self.del_frame,
                                                        )
                                        )
        self.home_button.pack(side='left', pady=(20, 0))


    def enter_name(self):
        self.button_frame.destroy()
        self.name_entry = ctk.CTkEntry(self.parent, width=250, height=35, placeholder_text='FirstName LastName')
        self.name_entry.pack(pady=10)
        self.folder_start = ctk.CTkButton(self.parent, width=50, text="GO", command=lambda: self.new_item_folder(self.name_entry.get()))
        self.folder_start.pack()
        self.home_button = ctk.CTkButton(self.parent,
                                text='BACK',
                                width=40,
                                command= lambda:self.homescreen(
                                                self.name_entry,
                                                self.folder_start
                                                )
                                )
        self.home_button.pack(side='left', pady=(20, 0))



    def new_item_folder(self, name):
        file_path = filedialog.askdirectory()
        new_folders = make_folders(file_path, name)
        if new_folders:
            for item in new_folders:
                print(f'The folder {item[0]} was created in {item[1]}')
        else:
            print("No new items were found")
        

    def homescreen(self, *args):
        for x in args:
            x.destroy()
        self.home_button.destroy()
        self.start_buttons()

