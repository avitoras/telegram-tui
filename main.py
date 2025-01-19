from textual.app import App, ComposeResult
from textual.widgets import Placeholder, Label, Static, Rule
from textual.containers import Horizontal, VerticalScroll, Vertical

class T_m():
    """Класс объекта тестового сообщения (Test_message)"""

    def __init__(self, text: str, user: int):
        """
        text - текст сообщения \n
        user - айди отправителя сообщения
        """

        self.text = text
        self.user = user

class T_u():
    """Класс объекта тестового пользователя(Test_user)"""

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

test_chats = [T_u("антон", 1, [T_m("привет", 0), T_m("как дела?", 1), T_m("норм", 0)]), 
              T_u("лёха", 2, [T_m("как выйти из вима", 2), T_m("хелп", 2), T_m("никак", 0)]), 
              T_u("нифига", 3, [T_m("слушай, а как там лёха", 3), T_m("нифига", 0), T_m("нифигадлыроарыарышщращгшырашырвшщарш", 3)])]

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
