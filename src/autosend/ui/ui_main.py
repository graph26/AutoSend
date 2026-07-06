import sys
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QImage, QPainter, QPen, QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QInputDialog,
    QColorDialog, QInputDialog, QMessageBox, QLabel, QPushButton, QDialog
)
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from webbrowser import open
import keyring
import logging
import asyncio
import datetime

if __name__ == '__main__':
    from autosend import Ui_MainWindow
    from widgets import WindowKey, WindowCreatePost
    from function import FunctionElementsGUI
else:
    from ui.autosend import Ui_MainWindow
    from ui.widgets import WindowKey, WindowCreatePost
    from ui.function import FunctionElementsGUI
    from core.bot_main import UserBotTelegram


class MainWindow(QMainWindow, Ui_MainWindow, FunctionElementsGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(r"src\autosend\ui\image\icon.png"))

        if keyring.get_password("system", "api_id") and keyring.get_password("system", "api_hash"):
            self.telegram_bot = UserBotTelegram(keyring.get_password("system", "api_id"),
                                                keyring.get_password("system", "api_hash"),
                                                keyring.get_password("system", "phone_number"))
        else:
            self.telegram_bot: UserBotTelegram

        self.add_function_menu()
        self.add_function()

    def add_function_menu(self):
        self.menu_file_key.setIcon(QIcon(r"src\autosend\ui\image\key.png"))
        self.menu_file_key.triggered.connect(self.input_key)
        self.menu_file_exit.triggered.connect(self.close)

        self.menu_help_github.setIcon(QIcon(r"src\autosend\ui\image\github.png"))
        self.menu_help_github.triggered.connect(lambda: open("https://github.com/graph26/AutoSend"))
        self.menu_help_telegram.setIcon(QIcon(r"src\autosend\ui\image\telegram.png"))
        self.menu_help_telegram.triggered.connect(lambda: open("https://t.me/I_teach_Python"))
        self.menu_help_discord.setIcon(QIcon(r"src\autosend\ui\image\discord.png"))
        self.menu_help_discord.triggered.connect(lambda: open("https://discord.gg/WtFGJTHU"))

        self.menu_tool_create.triggered.connect(self.create_post)

        self.menu_view_f11.triggered.connect(self.f11)
    
    def add_function(self):
        self.button_create.setIcon(QIcon(r"src\autosend\ui\image\tab.png"))
        self.button_create.clicked.connect(self.create_post)

        self.button_start.setIcon(QIcon(r'src\autosend\ui\image\play.png'))

        self.button_restore.setIcon(QIcon(r"src\autosend\ui\image\sync.png"))

        self.button_delete.setIcon(QIcon(r"src\autosend\ui\image\delete.png"))

        self.button_settings.setIcon(QIcon(r"src\autosend\ui\image\gear.png"))

    def button_start_function(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.telegram_bot.start())
        self.telegram_bot.shedular_start()

    
    def create_post(self):
        dialog = WindowCreatePost()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text, file, date = dialog.get_values()
            date = date.toPyDateTime()
            if not(date is None):
                self.telegram_bot.add_job(self.telegram_bot.send_post, DateTrigger(date))

    def f11(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


    def input_key(self):
        dialog = WindowKey()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            api_id, api_hash, phone_number = dialog.get_values()
            try:
                keyring.set_password("system", "api_id", api_id)
                keyring.set_password("system", "api_hash", api_hash)
                keyring.set_password("system", "phone_number", phone_number)
                self.telegram_bot = UserBotTelegram(keyring.get_password("system", "api_id"),
                                                keyring.get_password("system", "api_hash"),
                                                keyring.get_password("system", "phone_number"))
            except keyring.errors.PasswordSetError:
                logging.error("Ошибка сохранения данных")
            except Exception as e:
                logging.exception(f"{e}")

    def closeEvent(self, event):
        self.close()


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())