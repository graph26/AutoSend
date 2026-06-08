from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
import asynсio

class UserBotTelegram():
    def __init__(self, name: str, api_id: str, api_hash: str, phone_number: str):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

        self.bot: Client = Client(self.name, self.api_id,
                                self.api_hash, self.phone_number)
    

    def register_handlers(self):
        pass
        
    async def start(self):
        self.register_handlers(self)