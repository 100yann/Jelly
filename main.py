import customtkinter as ctk
from gui import Program


if __name__ == "__main__":
    root=ctk.CTk()
    root.geometry('720x480')
    root.config(padx=50, pady=50, background='light goldenrod')
    root.resizable(False, False)
    Program(root)
    root.mainloop()
