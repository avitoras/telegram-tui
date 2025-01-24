from textual.widgets import Input, Button, Label
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widget import Widget
from widgets.message import Message

class Dialog(Widget):
    def __init__(self, id=None, classes=None, disabled=False):
        super().__init__(id=id, classes=classes, disabled=disabled)

    def compose(self):
        with Vertical():
            with VerticalScroll(id="dialog"):
                yield Message(message="привет, я ыплыжлп", is_me=True)
                yield Message(message="о, дщытрапшщцрущ", is_me=False)
                yield Message(message="ДАТОУШЩАРШЩУРЩША!!!!", is_me=False)
                # должно быть примерно is_me = message.from_id == client.get_peer_id("me")
                # но я могу ошибаться, я это фиш если что
                #TODO: сделать кнопку чтобы прогрузить больше сообщений, но при этом чтобы при перезаходе в чат оставались прогруженными только 10 сообщений, а остальные декомпоузились

            with Horizontal(id="input_place"):
                yield Input(placeholder="Сообщение", id="msg_input")
                yield Button(label="➤", id="send", variant="primary")

    def on_button_pressed(self, event): # self добавил
        self.app.notify("Нажато отправить")
