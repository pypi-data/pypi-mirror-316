import tkinter as tk

class Entry:
    def __init__(self, parent):
        self.entry = tk.Entry(parent)

    def pack(self):
        self.entry.pack()

    def get_text(self):
        return self.entry.get()
