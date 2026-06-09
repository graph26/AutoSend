import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import json
from typing import TypedDict, cast

class StructureJsonTasks(TypedDict):
    messenger: list[str]
    chat_id: list[int | str]
    title: str | None
    text: str | None
    random: bool
    period: list[int]
    datetime: list[int]
    id: str


class AdvancedSchedular():
    telegram_task_dictionary: dict = {}
    max_task_dictionary: dict = {}

    def load_tasks(self) -> bool:
        try:
            with open(r"src\autosend\core\tasks.json", 'r', encoding="utf-8") as file:
                buffer = json.load(file)
                for task_i, data in buffer.items():
                    typed_data = cast(StructureJsonTasks, data)
                    if typed_data["datetime"] != []:
                        if datetime(*typed_data["datetime"]) < datetime.now():
                            continue
                    if "telegram" in typed_data["messenger"]:
                        self.telegram_task_dictionary.update([task_i, data])
                    if "max" in typed_data["messenger"]:
                        self.max_task_dictionary.update([task_i, data])
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
    
    def save_tasks(self):
        with open(r"src\autoosend\core\tasks.json", 'w', encoding="utf-8") as file:
            buffer = self.telegram_task_dictionary | self.max_task_dictionary
            json.dump(buffer, file, indent=4, ensure_ascii=False)
    
    