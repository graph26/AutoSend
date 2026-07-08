import sys
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt6.QtGui import QImage, QPainter, QPen, QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QInputDialog, QFormLayout, QButtonGroup,
    QColorDialog, QInputDialog, QMessageBox, QLabel, QPushButton, QDialog, QRadioButton, QHBoxLayout
)

class Parametrs(QDialog):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Параметры бота")
        self.setWindowIcon(QIcon(r"src\autosend\ui\image\icon.png"))
        self.setModal(True)

        layout = QFormLayout(self)

        group = QButtonGroup(self)
        self.text = 'markdown'
        self.rb_markdown = QRadioButton("MARKDOWN", self)
        self.rb_markdown.toggled.connect(self.handle_submit)
        self.rb_html = QRadioButton("HTML", self)
        self.rb_html.toggled.connect(self.handle_submit)
        
        group.addButton(self.rb_markdown)
        group.addButton(self.rb_html)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Отмена")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)
        

        layout.addRow("Выберите язык разметки:", group)

    def handle_submit(self):
        rb = self.sender()  
        if rb.isChecked():
            self.text = rb.text()
            print(f"Вы выбрали: {rb.text()}")
    
    def get_values(self) -> tuple:
        return 