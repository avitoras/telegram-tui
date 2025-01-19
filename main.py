from textual.app import App, ComposeResult
from textual.widgets import Placeholder, Label, Static, Rule
from textual.containers import Horizontal, VerticalScroll, Vertical
from telethon import TelegramClient, events, sync
from tokens import api_id, api_hash

names = []
soo = []

limits = 6

client = TelegramClient('Telegram-Cli', api_id, api_hash)
client.start()
print(client.get_me().stringify())

for titles in client.iter_dialogs(limit=limits):
    names.append('{:<14}'.format(titles.title))

for messages in client.iter_dialogs(limit=limits):
    soo.append('{:<14}'.format(messages.message.message))

class T_m():

    def __init__(self, text: str, user: int):
        """
        text - текст сообщения \n
        user - айди отправителя сообщения
        """

        self.text = text
        self.user = user

class T_u():

    def __init__(self, name: str, user_id: int, dialog: list[T_m]):
        """
        name - имя пользователя \n
        id - айди пользователя \n
        dialog - список сообщений (T_m) диалога
        """

        self.name = name
        self.user_id = user_id
        self.dialog = dialog

client = T_u("вы", 0, [])

test_chats = []

for i in range(0, limits):
    test_chats.append(T_u(names[i], 1, [T_m(soo[i], 0)]))

class Chat(Horizontal):
    """Кастомный виджет чата слева"""
    def __init__(self, user: T_u):
        super().__init__()
        self.user = user

    def _on_click(self):
        pass

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(f"┌───┐\n│ {self.user.name[:1]} │\n└───┘")
            with Vertical():
                yield Label(self.user.name, id="name")
                yield Label(self.user.dialog[-1].text)

class TelegramTUI(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Horizontal(id="chats"):
                with VerticalScroll():
                    for i in test_chats:
                        yield Chat(i)

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
