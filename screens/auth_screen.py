from textual.screen import Screen
from textual.widgets import Label, Input
from textual.containers import Vertical
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

class AuthScreen(Screen):
    """Класс логина в аккаунт"""

    def __init__(
            self, 
            name = None, 
            id = None, 
            classes = None, 
            telegram_client: TelegramClient | None = None
        ):
        super().__init__(name, id, classes)
        self.client = telegram_client

    def on_mount(self):
        self.ac = self.query_one("#auth_container")

    def compose(self):
        with Vertical(id="auth_container"):
            yield Label("Добро пожаловать в Telegram TUI")
            yield Input(placeholder="Номер телефона", id="phone")
            yield Input(placeholder="Код", id="code", disabled=True)
            yield Input(
                placeholder="Пароль", 
                id="password", 
                password=True, 
                disabled=True
            )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "phone":
            self.phone = event.value
            self.ac.query_one("#phone").disabled = True
            self.ac.query_one("#code").disabled = False
            await self.client.send_code_request(phone=self.phone)
        elif event.input.id == "code":
            try:
                self.code = event.value
                self.ac.query_one("#code").disabled = True
                await self.client.sign_in(phone=self.phone, code=self.code)
                self.app.pop_screen()
                self.app.push_screen("chats")
            except SessionPasswordNeededError:
                self.ac.query_one("#code").disabled = True
                self.ac.query_one("#password").disabled = False
        elif event.input.id == "password":
            self.password = event.value
            await self.client.sign_in(password=self.password)
            await self.client.start()
            self.app.pop_screen()
            self.app.push_screen("chats")
