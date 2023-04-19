import threading
from datetime import datetime
from pathlib import Path
from time import strftime

import serial
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QMainWindow,
                               QMessageBox, QPushButton)
from serial.tools import list_ports

from models import BasePanelData, MainValidator
from parse_radio import parse_radio
from ui.serial_saver import Ui_MainWindow

BAUDRATE = 115200


def get_comports_list() -> list[str]:
    return [i.name for i in list_ports.comports()]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.portsCombo.addItems([i.name for i in list_ports.comports()])
        self.refresh_button.clicked.connect(self.on_refresh_clicked)

        self.open_button.clicked.connect(self.open_port)

    def open_port(self):
        if self.portsCombo.currentText() != "":
            try:
                self.port = serial.Serial(
                    self.portsCombo.currentText(), baudrate=BAUDRATE
                )
            except serial.SerialException:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(
                    "Порт уже кто-то использует."
                    "Либо это вы - попробуйте потыкать кнопку Close,"
                    "либо ищите проблему в других программах"
                )
                msg.setWindowTitle("Error")
                msg.show()
            else:
                self.portTimer = QTimer(self)
                self.portTimer.timeout.connect(self.save_data)
                self.portTimer.setInterval(100)
                self.portTimer.start()

                self.data_save_folder = (
                    Path(__file__).parent / "data" / strftime("%d-%m-%Y_%H-%M-%S")
                )
                if not self.data_save_folder.parent.exists():
                    self.data_save_folder.parent.mkdir()

                if not self.data_save_folder.exists():
                    self.data_save_folder.mkdir()

    def close_port(self):
        self.port.close()
        self.portTimer.stop()

    def save_data(self):
        if self.port.in_waiting > 0:
            self._messageNumber = getattr(self, "_messageNumber", 0) + 1

            new_data = self.port.readline()

            self.textEdit.setText(self.textEdit.toPlainText() + f"{new_data.decode()}")
            sb = self.textEdit.verticalScrollBar()
            sb.setSliderPosition(sb.maximum())

            parsed_json_data = new_data.decode()
            parsed_json_data.replace("/r", "")
            parsed_json_data.replace("/n", "")

            parsed_json_data = parse_radio(parsed_json_data)
            parsed_json_data["number_message"] = self._messageNumber
            parsed_json_data = MainValidator.parse_obj(parsed_json_data)

            raw_file = self.data_save_folder / "raw.csv"
            json_file = self.data_save_folder / "parsed.json"

            with raw_file.open("ab") as file:
                file.write(new_data)

            with json_file.open("a") as file:
                file.write(parsed_json_data.json() + "\n")

    def on_refresh_clicked(self):
        self.portsCombo.clear()
        self.portsCombo.addItems([i.name for i in list_ports.comports()])


class App:
    def __init__(self) -> None:
        self.qapp = QApplication([])
        self.window = MainWindow()

    def start(self) -> None:
        self.window.show()
        self.qapp.exec()


if __name__ == "__main__":
    App().start()
