import tkinter as tk

class Window:
    def __init__(self, title="Py Crave GUI", width=400, height=300):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

    def add_component(self, component):
        component.pack()

    def run(self):
        self.root.mainloop()
