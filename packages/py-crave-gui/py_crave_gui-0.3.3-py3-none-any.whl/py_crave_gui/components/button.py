import tkinter as tk

class Button(tk.Button):  # Make sure it inherits from tk.Button
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, **kwargs)
        # Additional button setup can be added here if needed
