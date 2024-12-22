import tkinter as tk

class MenuBar:
    def __init__(self, master, menu_items):
        self.menu_bar = tk.Menu(master)
        for menu_name, commands in menu_items.items():
            menu = tk.Menu(self.menu_bar, tearoff=0)
            for command_name, command in commands:
                menu.add_command(label=command_name, command=command)
            self.menu_bar.add_cascade(label=menu_name, menu=menu)
        master.config(menu=self.menu_bar)
