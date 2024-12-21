import tkinter as tk

class Label:
    def __init__(self, parent, text):
        self.label = tk.Label(parent, text=text)

    def pack(self):
        self.label.pack()
