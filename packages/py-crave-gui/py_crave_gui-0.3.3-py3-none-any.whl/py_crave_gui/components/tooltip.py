import tkinter as tk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Bind events to show and hide the tooltip
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        """Display the tooltip when the user hovers over the widget."""
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty()
        width = self.widget.winfo_width()

        # Create a tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Remove window decorations
        self.tooltip_window.wm_geometry(f"+{x + width // 2}+{y + 25}")  # Position the tooltip

        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        """Hide the tooltip when the user stops hovering."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
