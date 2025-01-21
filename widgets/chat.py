from textual.widgets import Label
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.reactive import Reactive

class Chat(Widget):
    username = Reactive(" ", recompose=True)
    msg = Reactive(" ", recompose=True)
    peer_id = Reactive(0)

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(name=str(name), id=id, classes=classes, disabled=disabled)

    def _on_click(self):
        self.msg = str(self.peer_id)

    def compose(self):
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.username[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.username, id="name")
                yield Label(self.msg, id="last_msg")
