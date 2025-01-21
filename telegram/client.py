from telethon import TelegramClient, events, utils

class TelegramClientWrapper:
    def __init__(self, api_id, api_hash, message_handler):
        self.message_handler = message_handler
        self.client = TelegramClient('user', api_id, api_hash)
        self.client.on(events.NewMessage())(self.local_message_handler)

        #ни то ни то не работает, костя спаси

    async def local_message_handler(self, event):
        await self.message_handler()

    async def connect(self):
        await self.client.start()

    async def disconnect(self):
        await self.client.disconnect()

    async def get_dialogs(self, limit=10):
        dialogs_list = []
        async for dialog in self.client.iter_dialogs(limit=limit):
            dialogs_list.append(dialog)
        return [self._map_dialog(d) for d in dialogs_list]

    def _map_dialog(self, dialog):
        return DialogInfo(
            id=dialog.id,
            name=utils.get_display_name(dialog.entity),
            message=dialog.message
        )

class DialogInfo:
    def __init__(self, id, name, message):
        self.id = id
        self.name = name
        self.message = message
