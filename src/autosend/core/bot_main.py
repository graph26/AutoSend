from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.enums.parse_mode import *
import asyncio
import orjson
from datetime import datetime
from core.scheduler import *
import logging


class UserBotTelegram(AdvancedSchedular):
    def __init__(self, api_id: int | str, api_hash: str, phone_number: str, name: str="my_account"):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

        self.bot: Client = Client(self.name, self.api_id, self.api_hash, phone_number=self.phone_number, 
                                  ipv6=True, parse_mode=ParseMode.MARKDOWN)
        
    def load_tasks(self) -> bool:
        try:
            with open(r"src\autosend\core\tasks.json", 'r', encoding="utf-8") as file:
                buffer = orjson.load(file)
                for task_i, data in buffer.items():
                    if data["trigger"] == DateTrigger and data['next_run_time'] is None:
                        continue
                    job = Job(
                        data['id'],
                        data['name'],
                        data['func'],
                        data['args'],
                        data['kwargs'],
                        trigger=data["trigger"],
                        executor=data['executor'],
                        next_run_time=data['next_run_time'],
                    )
                    self.add_job(job)
            logging.info("Задачи загружены и включены в планировщик")
            return True
        except FileNotFoundError:
            logging.error("Не найден файл tasks.json")
            return False
        except Exception as e:
            logging.exception(f"{e}")
            return False
        
    def save_tasks(self) -> bool:
        try:
            with open(r"src\autoosend\core\tasks.json", 'w', encoding="utf-8") as file:
                buffer = {}
                for i, data in enumerate(self.get_jobs()):
                    typed_data = {}
                    typed_data["id"] = data.id
                    typed_data["name"] = data.name
                    typed_data["func"] = data.func
                    typed_data["args"] = data.args
                    typed_data["kwargs"] = data.kwargs
                    typed_data["trigger"] = data.trigger
                    typed_data["executor"] = data.executor
                    typed_data["next_run_time"] = data.next_run_time
                    buffer.update([f"task_{i}", typed_data])

                orjson.dump(buffer, file, indent=4, ensure_ascii=False)
            logging.info("Задачи успешно сохранены в json файл.")
            return True
        except Exception as e:
            logging.exception(f"{e}")
            return False

    async def handle_new_text_message(self, client, message):
        pass

    async def handle_start_command(self, client, message):
        await message.reply(f"Привет!")
    
    async def send_post(self, text: str, file: str):
        if file.endswith((".jpg", ".png", ".jpeg")):
            await self.bot.send_photo(, file, text, parse_mode=ParseMode.)
        await self.bot.send_message()
        

    def register_handlers(self):
        pass
        
    async def start(self):
        self.register_handlers(self)
        async with self.bot:
            await idle()