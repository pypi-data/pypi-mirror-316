import tkinter as tk

class Checkbox(tk.Checkbutton):
    def __init__(self, master, text, variable=None, **kwargs):
        # If no variable is provided, create a new BooleanVar
        if variable is None:
            variable = tk.BooleanVar()
        
        super().__init__(master, text=text, variable=variable, **kwargs)
        self.variable = variable  # Store the variable for later access

    def get_value(self):
        """Return the current value of the checkbox."""
        return self.variable.get()

    def set_value(self, value):
        """Set the value of the checkbox programmatically."""
        self.variable.set(value)
