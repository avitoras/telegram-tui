from textual.widgets import Label
from textual.containers import Horizontal, Vertical
from textual.widget import Widget

class Chat(Widget):
    def __init__(self, name: str | None = None, msg: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(name=str(name), id=id, classes=classes, disabled=disabled)
        self.msg = str(msg)

    def _on_click(self):
        pass

    def compose(self):
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.name[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.name, id="name")
                yield Label(self.msg, id="last_msg")
