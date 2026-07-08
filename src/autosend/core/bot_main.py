import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job
from apscheduler.triggers.base import BaseTrigger

from telethon import TelegramClient, events, connection
from datetime import datetime
from core.scheduler import *

from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import logging
logging.basicConfig(level=logging.INFO, filename="telegram_log.log", filemode="w",
                    format="%(name)s %(asctime)s %(levelname)s %(message)s")

class UserBotTelegram(QObject):

    status = pyqtSignal(bool)
    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, api_id: int | str, api_hash: str, phone_number: str, name: str="my_account",
                connection: type[connection.Connection] = connection.ConnectionTcpFull,
                proxy: tuple[str, int, str] | dict = None
                 ):
        super().__init__()
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.connection = connection
        self.proxy = proxy

        self.bot = None
        self._stop_requested = False
        self._scheduler = None


    @pyqtSlot()
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            self.bot = TelegramClient(self.name, self.api_id, self.api_hash, self.connection, True, self.proxy, loop=loop)
            self._scheduler = AsyncIOScheduler(event_loop=loop)

            async def send(chat: str | int, text: str, file: str = None):
                if not(file is None):
                    self.bot.send_file(chat, file, text)
                else:
                    await self.bot.send_message(chat, text, link_preview=False)

            @self.bot.on(events.NewMessage())
            async def handler_messages(event):
                if self._stop_requested:
                    if self._scheduler and self._scheduler.running:
                        self._scheduler.shutdown()
                    await self.bot.disconnect()
                    return

            with self.bot:
                self._scheduler.start()
                loop.run_until_complete(self.bot.run_until_disconnected())


        except Exception as exc:
            pass
        finally:
            if self._scheduler and self._scheduler.running:
               self._scheduler.shutdown()
            loop.close()

    async def add_task(self, chat: str | int, text: str, trigger, file: str=None):
        pass

        
    
    @pyqtSlot()
    def stop(self):
        self._stop_requested = True
       