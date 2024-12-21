import tkinter as tk
from tkinter import ttk

class ComboBox:
    def __init__(self, master, values, **kwargs):
        self.combo = ttk.Combobox(master, values=values, **kwargs)

    def pack(self, *args, **kwargs):
        """Expose the pack method for the ComboBox."""
        self.combo.pack(*args, **kwargs)

    def bind_select(self, callback):
        """Bind the Combobox selection event to a callback function."""
        self.combo.bind("<<ComboboxSelected>>", callback)

    def get(self):
        """Return the selected value of the ComboBox."""
        return self.combo.get()

    def set(self, value):
        """Set the value of the ComboBox."""
        self.combo.set(value)
