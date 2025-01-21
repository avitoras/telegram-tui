from telethon import TelegramClient, events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical, Container
from textual.widgets import Placeholder, Label, Static, Input, Button
from widgets.chat import Chat
from widgets.dialog import Dialog
from telegram.client import TelegramClientWrapper
from tokens import api_id, api_hash

class TelegramTUI(App):
    CSS_PATH = "../tcss/style.tcss"

    def __init__(self):
        super().__init__()
        self.telegram_client = TelegramClientWrapper(api_id, api_hash, self.update_chat_list)

    async def on_mount(self) -> None:
        self.chat_container = self.query_one("#main_container").query_one("#chats").query_one("#chat_container")

        self.limit = 25
        for i in range(self.limit):
            chat = Chat(id=f"chat-{i + 1}")
            self.chat_container.mount(chat)

        await self.telegram_client.connect()

    # TODO: скоро сюда переедет маунт чатов из функции on_mount
    def mount_chats(self):
        pass

    async def update_chat_list(self):
        dialogs = await self.telegram_client.get_dialogs(limit=self.limit)

        for i in range(len(dialogs)):
            chat = self.chat_container.query_one(f"#chat-{i + 1}")
            chat.username = str(dialogs[i].name)
            chat.msg = str(dialogs[i].message.message)
            chat.peer_id = dialogs[i].id
            #self.notify("Новое сообщение")    #колхоз дебаг

    def compose(self) -> ComposeResult:
        with Horizontal(id="main_container"):
            with Horizontal(id="chats"):
                yield VerticalScroll(Static(id="chat_container"))

            yield Dialog()

    async def on_exit_app(self):
        await self.telegram_client.disconnect()
        return super()._on_exit_app()
