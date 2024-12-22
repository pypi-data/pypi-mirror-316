from py_crave_gui.components.listbox import Listbox as BaseListbox

class EnhancedListbox(BaseListbox):
    def __init__(self, master, items=None, **kwargs):
        # Initialize the base Listbox
        super().__init__(master, items=items, **kwargs)

    def add_item(self, item):
        """Add an item to the listbox."""
        self.insert(item)

    def get_selected_index(self):
        """Get the index of the selected item."""
        selected = self.listbox.curselection()
        return selected[0] if selected else None

    def get_selected_item(self):
        """Get the value of the selected item."""
        index = self.get_selected_index()
        return self.listbox.get(index) if index is not None else None

    def delete(self, index):
        """Delete an item at the specified index."""
        self.listbox.delete(index)
