from telethon import TelegramClient, events, sync, utils
from textual.app import App, ComposeResult
from textual.widgets import Placeholder, Label, Static, Rule
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.reactive import var
from textual.widget import Widget
from tokens import api_id, api_hash

class Chat(Widget):
    """Кастомный виджет чата слева"""
    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def _on_click(self):
        pass

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.name[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.name, id="name")
                #yield Label(self.user.dialog[-1].text)

class TelegramTUI(App):

    CSS_PATH = "styles.tcss"
    
    def __init__(self):
        super().__init__()
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('user', api_id, api_hash)
        self.chats = var([])

    async def on_mount(self) -> None:
        await self.client.start()
        dialogs = []
        async for dialog in self.client.iter_dialogs():
            dialogs.append(dialog)
        self.chats = dialogs
        await self.update_chat_list()

    async def update_chat_list(self):
        #if self.chats:
        #for dialog in self.chats:
        #    name = utils.get_display_name(dialog.entity)
        #    last_msg = ""  # Значение по умолчанию

        #    try:
        #        last_messages = await self.client.get_messages(dialog.entity, limit=1)
        #        if last_messages:
        #            last_msg = last_messages[0].message  # Получаем текст последнего сообщения
        #    except Exception as e: #  Добавлена обработка ошибок
        #        print(f"Ошибка получения последнего сообщения: {e}")

        chat_container = self.query_one("#main_container").query_one("#chats").query_one("#chat_container")
        chat_container.query(Chat).remove()  # Clear existing labels

        for dialog in self.chats:
            name = utils.get_display_name(dialog.entity)
            #msg = utils.get_input_peer
            chat = Chat(name, id=f"chat-{dialog.id}")
            chat_container.mount(chat)

    def compose(self) -> ComposeResult:
        with Horizontal(id="main_container"):
            with Horizontal(id="chats"):
                yield VerticalScroll(*[Static(id="chat_container")])

                yield Rule("vertical")

            with VerticalScroll(id="dialog"):
                yield Placeholder(label="message", classes=("message"))
                yield Placeholder(label="message", classes=("message"))
                yield Placeholder(label="message", classes=("message"))
                yield Placeholder(label="message", classes=("message"))
                yield Placeholder(label="message", classes=("message"))

if __name__ == "__main__":
    app = TelegramTUI()
    app.run()
