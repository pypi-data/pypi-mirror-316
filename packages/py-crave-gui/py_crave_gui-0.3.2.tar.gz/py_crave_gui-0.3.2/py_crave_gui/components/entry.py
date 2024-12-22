# In py_crave_gui/components/entry.py
import tkinter as tk

class Entry(tk.Entry):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_variable = kwargs.get('textvariable', None)  # Get textvariable if provided
        if self.text_variable:
            self.config(textvariable=self.text_variable)  # Set the textvariable
