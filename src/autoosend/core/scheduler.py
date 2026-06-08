import asyncio
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import json

class AdvancedSchedular():
    telegram_task_dictionary: dict = {}
    max_task_dictionary: dict = {}

    def load_tasks(self):
        with open(r"src\autoosend\core\tasks.json", 'r', encoding="utf-8") as file:
            buffer = json.load(file)
            for task_i, data in buffer:
                if "telegram" in data["messenger"]:
                    
                    self.telegram_task_dictionary.update([task_i, data])
                if "max" in data["messenger"]:
                    self.max_task_dictionary.update([task_i, data])
    
    def save_tasks(self):
        with open(r"src\autoosend\core\tasks.json", 'w', encoding="utf-8") as file:
            buffer = self.telegram_task_dictionary | self.max_task_dictionary
            json.dump(buffer, file, indent=4, ensure_ascii=False)
    
