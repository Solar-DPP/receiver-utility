from pathlib import Path

from serial.tools import list_ports
from models import MainValidator
from parse_radio import parse_radio
import plotly.graph_objs as go
from math import sin
import numpy as np
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QPushButton
from plotly.graph_objects import Figure, Scatter
import plotly

import numpy as np

from untitled import Ui_MainWindow


example_ = (Path(__file__).parent / "radio_example.txt").read_text()

model = MainValidator.parse_obj(parse_radio(example_))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.portsCombo.addItems([i.name for i in list_ports.comports()])
        self.refresh_button.clicked.connect(self.on_refresh_clicked)
        
    def on_refresh_clicked(self):
        self.portsCombo.clear()
        self.portsCombo.addItems([i.name for i in list_ports.comports()])

        
        """        # some example data
        x = np.arange(1000)
        y = x**2

        # create the plotly figure
        fig = Figure(Scatter(x=x, y=y))

        # we create html code of the figure
        html = '<html><body>'
        html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        html += '</body></html>'

        # we create an instance of QWebEngineView and set the html code
        plot_widget = QWebEngineView()
        plot_widget.setHtml(html)"""


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

