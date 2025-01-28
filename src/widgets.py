"""Файл с кастомными виджетами приложения"""

from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual.widget import Widget
from textual.reactive import Reactive
from textual.widgets import Input, Button, Label
from telethon import TelegramClient, events, utils

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
        global personid
        personid = 0
        self.notify = notify_fun
        
    def _on_click(self):
        global personid
        self.msg = str(self.peer_id)
        personid = int(self.peer_id)
        self.app.notify("нажат чат")

    def compose(self):
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.username[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.username, id="name")
                yield Label(self.msg, id="last_msg")

class Dialog(Widget):
    """Класс окна диалога"""
    
    def __init__(self, id=None, classes=None, disabled=False, telegram_client: TelegramClient | None = None):
        global personid
        super().__init__(id=id, classes=classes, disabled=disabled)
        self.telegram_client = telegram_client
        self.personid = personid
        
    async def load_messages(self):
        self.messages = []
        for messages1 in self.telegram_client.iter_dialogs(self.personid, limit=5):
            messages.append(messages1.text)

    def compose(self):
        messages = self.messages
        with Vertical():
            with VerticalScroll(id="dialog"):
                yield Message(message=messages[0], is_me=True)
                yield Message(message=messages[1], is_me=False)
                yield Message(message=messages[2], is_me=False)
                yield Message(message=messages[3], is_me=True)
                yield Message(message=messages[4], is_me=False)

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

    async def on_button_pressed(self, event): # self добавил
        self.app.notify("Нажато отправить")
        self.message_text = self.query_one("#msg_input").value
        await self.telegram_client.send_message(personid, str(self.message_text))

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
