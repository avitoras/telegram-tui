from textual.widgets import Label
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.reactive import Reactive

class Chat(Widget):
    """Класс виджета чата для панели чатов"""

    username = Reactive(" ", recompose=True)
    msg = Reactive(" ", recompose=True)
    peer_id = Reactive(0)

    def __init__(self, name: str | None = None, notify_func = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(name=str(name), id=id, classes=classes, disabled=disabled)
        self.notify = notify_func

    def _on_click(self):
        self.msg = str(self.peer_id)
        self.notify("нажат чат")

    def compose(self):
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.username[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.username, id="name")
                yield Label(self.msg, id="last_msg")
