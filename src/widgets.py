"""Файл с кастомными виджетами приложения"""

from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual.widget import Widget
from textual.reactive import Reactive
from textual.widgets import Input, Button, Label, Static
from telethon import TelegramClient, events

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
    
    def __init__(
            self, 
            id=None, 
            classes=None, 
            disabled=None, 
            telegram_client: TelegramClient | None = None
        ):
        super().__init__(id=id, classes=classes, disabled=disabled)
        self.telegram_client = telegram_client
        self.chat_id = -1002299818671
        self.is_msg_update_blocked = False

    async def on_mount(self):
        self.limit = 30

        self.msg_input = self.query_one("#msg_input")
        self.dialog = self.query_one(Vertical).query_one("#dialog")

        self.me = await self.telegram_client.get_me()

        await self.update_dialog()

        for event in (
            events.NewMessage, 
            events.MessageDeleted, 
            events.MessageEdited
        ):
            self.telegram_client.on(event(chats=(self.chat_id)))\
                (self.update_dialog)

    def mount_messages(self, limit: int):
        print("Загрузка виджетов сообщений...")

        msg_amount = len(self.dialog.query(Message))

        if limit > msg_amount:
            for i in range(limit - msg_amount):
                self.dialog.mount(Message(id=f"msg-{i + msg_amount + 1}"))
        elif limit < msg_amount:
            for i in range(msg_amount - limit):
                self.dialog.query(Message).last().remove()

    async def update_dialog(self, event = None):
        print("Запрос обновления сообщений")

        if not self.is_msg_update_blocked:
            self.is_msg_update_blocked = True

            messages = await self.telegram_client.get_messages(
                entity=self.chat_id, limit=self.limit
            )
            print("Получены сообщения")

            limit = len(messages)
            self.mount_messages(limit)

            for i in range(limit):
                chat = self.dialog.query_one(f"#msg-{i + 1}")
                chat.message = str(messages[i].message) + \
                    (not str(messages[i].message)) * " "
                chat.is_me = messages[i].from_id == self.me.id
                chat._update_styles()

            self.is_msg_update_blocked = False
            print("Сообщения обновлены")
        else:
            print("Обновление сообщений невозможно: уже выполняется")

    def compose(self):
        with Vertical():
            yield VerticalScroll(id="dialog")
            with Horizontal(id="input_place"):
                yield Input(placeholder="Сообщение", id="msg_input")
                yield Button(label="➤", id="send", variant="primary")

    async def on_button_pressed(self, event = None):
        await self.send_message()
    
    async def on_input_submitted(self, event = None):
        await self.send_message()

    async def send_message(self):
        await self.telegram_client.send_message(
            self.chat_id, 
            str(self.msg_input.value)
        )
        self.msg_input.value = ""
        await self.update_dialog()

class Message(Widget):
    """Класс виджета сообщений для окна диалога"""

    message = Reactive("", recompose=True)
    is_me = Reactive(False, recompose=True)
    
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
        label_border = container.query_one(".border")
        if self.is_me:
            self.styles.padding = (0, 0, 0, 15)
            container.styles.align_horizontal = "right"
            label_border.styles.border = ("solid", "#4287f5")
        else:
            self.styles.padding = (0, 15, 0, 0)
            container.styles.align_horizontal = "left"
            label_border.styles.border = ("solid", "#ffffff")

    def compose(self):
        with Container():
            with Static(classes="border"):
                yield Static(str(self.message))
