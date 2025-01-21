from textual.widgets import Label
from textual.containers import Container
from textual.widget import Widget

class Message(Widget):
    def __init__(self, name=None, message=None, is_me=None, id=None, classes=None, disabled=False):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.message = message
        self.is_me = is_me

    def on_mount(self):
        container = self.query_one(Container)
        label = container.query_one(Label)
        if self.is_me:
            self.styles.padding = (0, 0, 0, 15)
            label.styles.text_align = "right"
            container.styles.align_horizontal = "right"
            label.styles.border = ("solid", "#4287f5")
        else:
            self.styles.padding = (0, 15, 0, 0)
            label.styles.text_align = "left"
            container.styles.align_horizontal = "left"
            label.styles.border = ("solid", "#ffffff")

    def compose(self):
        with Container():
            yield Label(str(self.message))
