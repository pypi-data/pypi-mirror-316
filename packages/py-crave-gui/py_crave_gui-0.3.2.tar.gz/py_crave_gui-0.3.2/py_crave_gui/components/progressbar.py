import tkinter as tk
from tkinter.ttk import Progressbar

class ProgressBar(Progressbar):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self['maximum'] = 100  # Set maximum value for the progress bar
        self['value'] = 0      # Set initial value

    def set_value(self, value):
        """Set the value of the progress bar."""
        self['value'] = value
