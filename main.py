from telethon import TelegramClient, events, utils
from textual.app import App, ComposeResult
from textual.widgets import Placeholder, Label, Static, Rule, Input, Button
from textual.containers import Horizontal, VerticalScroll, Vertical, Container
from textual.reactive import var
from textual.widget import Widget
from tokens import api_id, api_hash

class Chat(Widget):
    """Кастомный виджет чата слева"""

    def __init__(self, name: str | None = None, msg: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(name=str(name), id=id, classes=classes, disabled=disabled)
        self.msg = str(msg)

    def _on_click(self):
        pass

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.name[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.name, id="name")
                yield Label(self.msg, id="last_msg")

class Dialog(Widget):
    """Кастомный виджет диалога справа"""

    def __init__(self, name = None, id = None, classes = None, disabled = False):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def compose(self):
        with Vertical():
            with VerticalScroll(id="dialog"):
                yield Message(message="привет, я ыплыжлп", is_me=True)
                yield Message(message="о, дщытрапшщцрущ", is_me=False) 
                yield Message(message="ДАТОУШЩАРШЩУРЩША!!!!", is_me=False) 
                #должно быть примерно is_me = message.from_id == client.get_peer_id("me")
                #но я могу ошибаться, я это фиш если что
            
            with Horizontal(id="input_place"):
                yield Input(placeholder="Сообщение", id="msg_input")
                yield Button(label="➤", id="send", variant="primary")

    def on_button_pressed(event):
        app.notify("Нажато отправить")


class Message(Widget):
    """Кастомный виджет сообщения"""

    def __init__(self, name = None, message = None, is_me = None, id = None, classes = None, disabled = False):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.message = message
        self.is_me = is_me

    def _on_mount(self):
        if self.is_me:
            self.styles.padding = (0, 0, 0, 15)
            self.query_one(Container).query_one(Label).styles.text_align = "right"
            self.query_one(Container).styles.align_horizontal = "right"
            self.query_one(Container).query_one(Label).styles.border = ("solid", "#4287f5")
        else:
            self.styles.padding = (0, 15, 0, 0)
            self.query_one(Container).query_one(Label).styles.text_align = "left"
            self.query_one(Container).styles.align_horizontal = "left"
            self.query_one(Container).query_one(Label).styles.border = ("solid", "#ffffff")

    def compose(self):
        with Container():
            #yield Label(self.message.message)  #это нормальный вариант
            yield Label(str(self.message))      #это тестовый вариант

class TelegramTUI(App):
    """Главный класс приложения"""

    CSS_PATH = "styles.tcss"
    
    def __init__(self):
        super().__init__()
        self.api_id = api_id
        self.api_hash = api_hash
        self.chats = []
        self.client = TelegramClient('user', api_id, api_hash)
        self.client.on(events.NewMessage())(self.handler)

    async def on_mount(self) -> None:
        await self.client.start()
        await self.update_chat_list()

    async def handler(self, event):
        await self.update_chat_list()

    async def update_chat_list(self):
        dialogs = []
        async for dialog in self.client.iter_dialogs(limit=10):
            dialogs.append(dialog)

        chat_container = self.query_one("#main_container").query_one("#chats").query_one("#chat_container")
        chat_container.query(Chat).remove()

        for dialog in dialogs:
            name = utils.get_display_name(dialog.entity)
            msg = dialog.message.message
            chat = Chat(name, msg, id=f"chat-{dialog.id}")
            chat_container.mount(chat)

    def compose(self) -> ComposeResult:
        with Horizontal(id="main_container"):
            with Horizontal(id="chats"):
                yield VerticalScroll(*[Static(id="chat_container")])

                yield Rule("vertical")

            yield Dialog()

    async def _on_exit_app(self):
        await self.client.disconnect()
        return super()._on_exit_app()

if __name__ == "__main__":
    app = TelegramTUI()
    app.run()
