# py_crave_gui/window.py

import tkinter as tk

class Window:
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)

    def add_component(self, component):
        component.pack()

    def add_menu(self, menu):
        menubar = tk.Menu(self.root)
        for menu_name, menu_items in menu:
            submenu = tk.Menu(menubar, tearoff=0)
            for item_name, item_command in menu_items:
                submenu.add_command(label=item_name, command=item_command)
            menubar.add_cascade(label=menu_name, menu=submenu)
        self.root.config(menu=menubar)

    def quit(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()
