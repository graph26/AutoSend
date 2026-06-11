from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
import asynсio
import json
from typing import TypedDict, cast
from datetime import datetime
from scheduler import *

class StructureJsonTasks(TypedDict):
    id: str
    name: str
    func: callable
    args: tuple
    kwargs: dict
    trigger: BaseTrigger
    executor: str
    next_run_time: datetime | None

class UserBotTelegram(AdvancedSchedular):
    def __init__(self, name: str, api_id: str, api_hash: str, phone_number: str):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

        self.bot: Client = Client(self.name, self.api_id,
                                self.api_hash, self.phone_number)
        
    def load_tasks(self) -> bool:
        try:
            with open(r"src\autosend\core\tasks.json", 'r', encoding="utf-8") as file:
                buffer = json.load(file)
                for task_i, data in buffer.items():
                    typed_data = cast(StructureJsonTasks, data)
                    if typed_data["trigger"] == DateTrigger and typed_data["next_run_time"] is None:
                        continue
                    job = Job(
                        typed_data["id"],
                        typed_data["name"],
                        typed_data["func"],
                        typed_data["args"],
                        typed_data["kwargs"],
                        trigger=typed_data["trigger"],
                        executor=typed_data["executor"],
                        next_run_time=typed_data["next_run_time"],
                    )
                    self.add_job(job)

            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
        
    def save_tasks(self) -> bool:
        try:
            with open(r"src\autoosend\core\tasks.json", 'w', encoding="utf-8") as file:
                buffer = {}
                for i, data in enumerate(self.get_jobs()):
                    typed_data = cast(StructureJsonTasks, typed_data)
                    typed_data["id"] = data.id
                    typed_data["name"] = data.name
                    typed_data["func"] = data.func
                    typed_data["args"] = data.args
                    typed_data["kwargs"] = data.kwargs
                    typed_data["trigger"] = data.trigger
                    typed_data["executor"] = data.executor
                    typed_data["next_run_time"] = data.next_run_time
                    buffer.update([f"task_{i}", typed_data])

                json.dump(buffer, file, indent=4, ensure_ascii=False)

            return True
        except Exception as e:
            return False

    async def handle_new_text_message(self, client, message):
        pass

    async def handle_start_command(self, client, message):
        await message.reply(f"Привет!")
    
    async def send_post(self):
        await self.bot.send_message()
        

    def register_handlers(self):
        pass
        
    async def start(self):
        self.register_handlers(self)
        async with self.bot:
            await idle()