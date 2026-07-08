from config import *
from core.bot_main import *
from ui.ui_main import *
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO, filename="system_log.log", filemode="w", encoding='utf-8',
                    format="%(name)s %(asctime)s %(levelname)s %(message)s")

def get_logger(name: str, filename: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Защита от дублирования хендлеров при повторном вызове
    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        LOG_DIR / filename,
        maxBytes=5 * 1024 * 1024,  # 5 МБ
        backupCount=3,
        encoding="utf-8"
    )
    handler.setLevel(level)

    formatter = logging.Formatter(
        "%(name)s %(asctime)s %(levelname)s %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def main():
    logging.info("Запуск приложения (gui)")
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()