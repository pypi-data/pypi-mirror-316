# py_crave_gui/components/listbox.py

import tkinter as tk

class Listbox(tk.Listbox):
    def __init__(self, parent, items, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.items = items
        self.insert_items(items)

    def insert_items(self, items):
        """Insert each item in the listbox."""
        for item in items:
            self.insert(tk.END, item)

    def get_value(self):
        """Return the currently selected value."""
        try:
            return self.get(self.curselection())
        except IndexError:
            return None

    def set_value(self, value):
        """Set the selected value in the listbox."""
        try:
            index = self.items.index(value)
            self.select_set(index)
        except ValueError:
            pass
