class Theme:
    def __init__(self, name):
        self.name = name
        self.styles = {}

    def set_style(self, widget_class, **styles):
        self.styles[widget_class] = styles

    def apply(self, app):
        for widget_class, style in self.styles.items():
            for widget in app.components:
                if isinstance(widget, widget_class):
                    widget.config(style)
