from config import *
from .core.bot_main import *
from .ui.ui_main import MainWindow
import logging

logging.basicConfig(level=logging.INFO, filename="system_log.log", filemode="w",
                    format="%(name)s %(asctime)s %(levelname)s %(message)s")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()