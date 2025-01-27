"""Файл с кастомными виджетами приложения"""

from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual.widget import Widget
from textual.reactive import Reactive
from textual.widgets import Input, Button, Label

class Chat(Widget):
    """Класс виджета чата для панели чатов"""

    username = Reactive(" ", recompose=True)
    msg = Reactive(" ", recompose=True)
    peer_id = Reactive(0)

    def __init__(
            self, 
            name: str | None = None, 
            id: str | None = None, 
            classes: str | None = None, 
            disabled: bool = False
    ):
        super().__init__(
            name=str(name), 
            id=id, 
            classes=classes, 
            disabled=disabled
        )
    
    def _on_click(self):
        self.msg = str(self.peer_id)
        self.app.notify("нажат чат")

    def compose(self):
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.username[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.username, id="name")
                yield Label(self.msg, id="last_msg")

class Dialog(Widget):
    """Класс окна диалога"""
    
    def __init__(self, id=None, classes=None, disabled=False):
        super().__init__(id=id, classes=classes, disabled=disabled)

    def compose(self):
        with Vertical():
            with VerticalScroll(id="dialog"):
                yield Message(message="привет, я ыплыжлп", is_me=True)
                yield Message(message="о, дщытрапшщцрущ", is_me=False)
                yield Message(message="ДАТОУШЩАРШЩУРЩША!!!!", is_me=False)
                # должно быть примерно
                # is_me = message.from_id == client.get_peer_id("me")

                # но я могу ошибаться, я это фиш если что

                #TODO: сделать кнопку чтобы прогрузить больше сообщений,
                #но при этом чтобы при перезаходе в чат оставались 
                #прогруженными только 10 сообщений, 
                #а остальные декомпоузились

            with Horizontal(id="input_place"):
                yield Input(placeholder="Сообщение", id="msg_input")
                yield Button(label="➤", id="send", variant="primary")

    def on_button_pressed(self, event): # self добавил
        self.app.notify("Нажато отправить")

class Message(Widget):
    """Класс виджета сообщений для окна диалога"""
    
    def __init__(
            self, 
            name=None, 
            message=None, 
            is_me=None, 
            id=None, 
            classes=None, 
            disabled=False
        ):
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
