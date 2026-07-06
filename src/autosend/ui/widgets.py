from PyQt6.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal, QDateTime
from PyQt6.QtGui import QImage, QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog, QVBoxLayout, QLineEdit, QDateTimeEdit, QWidget,
    QMessageBox, QLabel, QPushButton, QDialog, QHBoxLayout, QFormLayout, QTextEdit
)

class WidgetDateAndTime(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор даты и времени")
        self.setWindowIcon(QIcon(r"src\autosend\ui\image\icon.png"))

        self.datetime_edit = QDateTimeEdit(self)
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())

        layout = QVBoxLayout()
        layout.addWidget(self.datetime_edit)
        self.setLayout(layout)

        self.datetime_edit.dateTimeChanged.connect(self.onDateTimeChanged)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

    def onDateTimeChanged(self, datetime):
        print("Дата и время изменены:", datetime.toString())
    
    def get_selected_datetime(self):
        return self.datetime_edit.dateTime()


class WindowCreatePost(QDialog):
    valuesEntered = pyqtSignal(str, str, QDateTime)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание поста")
        self.setWindowIcon(QIcon(r"src\autosend\ui\image\icon.png"))
        self.setModal(True)

        layout = QFormLayout(self)

        self.message = QTextEdit()
        self.image = QPushButton("Выбрать")
        self.image.clicked.connect(self.input_file)
        self.date_and_time = QPushButton("Выбрать")
        self.date_and_time.clicked.connect(self.date_time)

        self.selected_datetime_label = QLabel("Не выбрано")
        self.selected_datetime_label.setWordWrap(True)

        self.selected_file_path = ""
        self.selected_datetime_obj = None

        layout.addRow("Введите текст:", self.message)
        layout.addRow("Выберите изображение/видео/gif:", self.image)
        layout.addRow("Выберите дату и время отправления:", self.date_and_time)
        layout.addRow("Выбранное время:", self.selected_datetime_label)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)

    def get_values(self) -> tuple[str, str, QDateTime]:
        return self.message.text(), self.selected_file_path, self.selected_datetime_obj
    
    def date_time(self):
        self.datetime_edit = WidgetDateAndTime()
        if self.datetime_edit.exec() == QDialog.DialogCode.Accepted:
            selected_datetime = self.datetime_edit.get_selected_datetime()
            if selected_datetime:
                self.selected_datetime_obj = selected_datetime

                self.selected_datetime_label.setText(selected_datetime.toString("yyyy-MM-dd HH:mm:ss"))
            else:
                 print("Диалог был отменен или не содержит дату.")

    def input_file(self):
        file, ok = QFileDialog.getOpenFileNames(
            self,
            "Выберите файл(ы)",
            ".",
            "Image File (*.png *.jpg *.jpeg);; Video File (*.mp4 *.gif);; All Files (*)"
        )
        self.selected_file_path = file


class WindowKey(QDialog):
    valuesEntered = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Введите ключи")
        self.icon = QIcon(QPixmap(r"src\autosend\ui\image\icon.png"))
        self.setWindowIcon(self.icon)

        layout = QFormLayout(self)

        self.api_id_input = QLineEdit()
        self.api_hash_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setMaxLength(16)

        layout.addRow("api_id:", self.api_id_input)
        layout.addRow("api_hash:", self.api_hash_input)
        layout.addRow("Номер телефона:", self.phone_number_input)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)

    def get_values(self) -> tuple[str, str, str]:
        return self.api_id_input.text(), self.api_hash_input.text(), self.phone_number_input.text()