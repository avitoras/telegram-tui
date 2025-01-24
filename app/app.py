#from telethon import TelegramClient, events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static, Footer
from widgets.chat import Chat
from widgets.dialog import Dialog
from telegram.client import TelegramClientWrapper
from tokens import api_id, api_hash

class TelegramTUI(App):
    CSS_PATH = "../tcss/style.tcss"

    def __init__(self):
        super().__init__()
        

    async def on_mount(self) -> None:
        self.telegram_client = TelegramClientWrapper(api_id, api_hash, self.update_chat_list)
        self.chat_container = self.query_one("#main_container").query_one("#chats").query_one("#chat_container")
        self.limit = 100
        for i in range(self.limit):
            chat = Chat(id=f"chat-{i + 1}")
            self.chat_container.mount(chat)
        #self.mount_chats(limit=25)

        await self.telegram_client.connect()

        await self.update_chat_list()

    # TODO: скоро сюда переедет маунт чатов из функции on_mount
    # P.S. сделано, но неудачно
    def mount_chats(self, limit: int):
        self.limit = limit
        chats_amount = len(self.chat_container.query(Chat))
        if limit > chats_amount:
            for i in range(limit - chats_amount):
                chat = Chat(id=f"chat-{i + 1 + (limit - chats_amount)}")
                self.chat_container.mount(chat)
        elif not (limit == chats_amount):
            for i in range(chats_amount - limit):
                self.chat_container.query(Chat).last().remove()

    async def update_chat_list(self):
        dialogs = await self.telegram_client.get_dialogs(limit=self.limit)

        for i in range(len(dialogs)):
            chat = self.chat_container.query_one(f"#chat-{i + 1}")
            chat.username = str(dialogs[i].name)
            chat.msg = str(dialogs[i].message.message)
            chat.peer_id = dialogs[i].id
            #self.notify("Новое сообщение")    #колхоз дебаг

    def compose(self) -> ComposeResult:
        yield Footer()
        with Horizontal(id="main_container"):
            with Horizontal(id="chats"):
                yield VerticalScroll(Static(id="chat_container"))
                #TODO: сделать кнопку чтобы прогрузить больше чатов, это оптимизация

            yield Dialog()

    async def on_exit_app(self):
        await self.telegram_client.disconnect()
        return super()._on_exit_app()
