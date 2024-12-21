import tkinter as tk

class RadioButton:
    def __init__(self, master, text, value, variable, command=None, options=None, **kwargs):
        """
        A custom RadioButton class that creates multiple radio buttons.
        :param master: The parent widget.
        :param text: The label text for the radio button.
        :param value: The value associated with the radio button.
        :param variable: A tkinter variable (e.g., StringVar, IntVar) to hold the selected value.
        :param command: A callback function when the radio button is selected.
        :param options: A list of options for the radio buttons (optional).
        :param kwargs: Other keyword arguments passed to the Radiobutton widget.
        """
        # Set up the initial radio button
        self.variable = variable
        self.command = command
        self.master = master
        
        # If no options are provided, only use the given value for this single button
        self.options = options if options else [value]
        
        # List to hold the created radio buttons
        self.buttons = []

        # Create a RadioButton for each option
        for option in self.options:
            button = tk.Radiobutton(master, text=option, value=option, variable=self.variable, command=self.command, **kwargs)
            self.buttons.append(button)

    def add_to_parent(self):
        """Place all radio buttons in the parent using pack()"""
        for button in self.buttons:
            button.pack()

    def get_value(self):
        """Return the value of the selected radio button"""
        return self.variable.get()

    def set_value(self, value):
        """Set the value of the radio button"""
        self.variable.set(value)
