# py_crave_gui/components/slider.py

import tkinter as tk

class Slider(tk.Scale):
    def __init__(self, parent, min_value=0, max_value=100, initial_value=50, orient=tk.HORIZONTAL, *args, **kwargs):
        super().__init__(parent, from_=min_value, to=max_value, orient=orient, *args, **kwargs)
        self.set(initial_value)  # Set the initial value of the slider

    def get_value(self):
        """Return the current value of the slider."""
        return self.get()

    def set_value(self, value):
        """Set the value of the slider."""
        self.set(value)
