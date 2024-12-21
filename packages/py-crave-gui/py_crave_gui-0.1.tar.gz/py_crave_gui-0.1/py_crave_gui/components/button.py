import tkinter as tk

class Button:
    def __init__(self, parent, text, command=None):
        self.button = tk.Button(parent, text=text, command=command)

    def pack(self):
        self.button.pack()
