import json
from pathlib import Path
from typing import Iterable, Sequence
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication, QDialog, QMessageBox
from models import MainValidator
from parse_radio import ParseError, parse_radio

from ui.plotter_select import Ui_MainWindow

class StartPlotWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.plotButton.clicked.connect(self.clicked)

    def clicked(self):
        file_name, _ = QFileDialog().getOpenFileName()
        file_path = Path(file_name)
        
        data = file_path.read_text()

        q = False

        splitted = data.split("\n")[:-2]

        if file_path.suffix in (".txt", ".csv"):
            data.replace("\r", "")
            data = []
            for i in range(1, len(splitted)+1):
                try:
                    pars = parse_radio(splitted[i-1])
                except ParseError:
                    continue

                pars["number_message"] = i

                data.append(pars)
                

        elif file_path.suffix == ".json":
            data = (json.loads(i) for i in splitted)
        else:
            q = True

        if q:
            dialog = QMessageBox()
            
            dialog.setIcon(QMessageBox.Critical)
            dialog.setText("Error")
            dialog.setWindowTitle("Error")
            dialog.setInformativeText("Короче, ты мне кажись что-то не то подсунул. Мне надо .json или .csv")
            dialog.exec()
        else:
            data_iterator = (MainValidator.parse_obj(i) for i in data)

            plot(data_iterator)
        

def plot(data: Iterable[MainValidator]):
    time_start_data = []

    power_lenses_data = []
    power_standard_data = []

    amperage_lenses_data = []
    amperage_standard_data = []

    voltage_lenses_data = []
    voltage_standard_data = []

    li_top_left = []
    li_bottom_left = []
    li_top_right = []
    li_bottom_right = []
    
    temp_lenses = []
    temp_standard = []

    x_data = []
    y_data = []

    for item in data:
        time_start_data.append(item.time / 1000)
        
        power_lenses_data.append(item.lenses_panels.voltage*item.lenses_panels.amperage*1000)
        power_standard_data.append(item.standard_panels.voltage*item.standard_panels.amperage*1000)

        amperage_lenses_data.append(item.lenses_panels.amperage*1000)
        amperage_standard_data.append(item.standard_panels.amperage*1000)

        voltage_lenses_data.append(item.lenses_panels.voltage)
        voltage_standard_data.append(item.standard_panels.voltage)

        li_top_left.append(item.light_intensity.top_left)
        li_bottom_left.append(item.light_intensity.bottom_left)
        li_top_right.append(item.light_intensity.top_right)
        li_bottom_right.append(item.light_intensity.bottom_right)

        temp_lenses.append(item.lenses_panels.temperature)
        temp_standard.append(item.standard_panels.temperature)

        x_data.append(item.lenses_panels.x)
        y_data.append(item.lenses_panels.y)
        
    
    energy_fig = make_subplots(rows=2, cols=2,
                               specs=[[{"rowspan": 2}, {}],
                                    [None, {}]],
                               subplot_titles=("Мощность вырабатываемая панельками",
                                             "Напряжение на панельках",
                                             "Сила тока на панельках"),)

    energy_fig.add_trace(go.Scatter(x=time_start_data, y=power_lenses_data,
                                    legendgroup="lenses", line=dict(color='blue'), name="Панельки с линзами"), row=1, col=1)
    energy_fig.add_trace(go.Scatter(x=time_start_data, y=power_standard_data,
                                    legendgroup="standard", line=dict(color='red'), name="Панельки без линз"), row=1, col=1)
    
    energy_fig.update_xaxes(title_text="Секунды", row = 1, col = 1)
    energy_fig.update_yaxes(title_text="милиВатты", row = 1, col = 1)

    energy_fig.add_trace(go.Scatter(x=time_start_data, y=voltage_lenses_data,
                                    legendgroup="lenses", line=dict(color='blue'),
                                    showlegend=False), row=1, col=2)
    energy_fig.add_trace(go.Scatter(x=time_start_data, y=voltage_standard_data,
                                    legendgroup="standard", line=dict(color='red'),
                                    showlegend=False), row=1, col=2)
    energy_fig.update_xaxes(title_text="Секунды", row = 1, col = 2)
    energy_fig.update_yaxes(title_text="Вольты", row = 1, col = 2)

    energy_fig.add_trace(go.Scatter(x=time_start_data, y=amperage_lenses_data,
                                    legendgroup="lenses", line=dict(color='blue'),
                                    showlegend=False), row=2, col=2)
    energy_fig.add_trace(go.Scatter(x=time_start_data, y=amperage_standard_data,
                                    legendgroup="standard", line=dict(color='red'),
                                    showlegend=False), row=2, col=2)
    energy_fig.update_xaxes(title_text="Секунды", row = 2, col = 2)
    energy_fig.update_yaxes(title_text="милиАмперы", row = 2, col = 2)

    li_fig = make_subplots(subplot_titles=["Освещённость с фотодатчиков"])

    li_fig.add_trace(go.Scatter(x=time_start_data, y=li_top_left, name="Лево верх"))
    li_fig.add_trace(go.Scatter(x=time_start_data, y=li_bottom_left, name="Лево низ"))
    li_fig.add_trace(go.Scatter(x=time_start_data, y=li_top_right, name="Право верх"))
    li_fig.add_trace(go.Scatter(x=time_start_data, y=li_bottom_right, name="Право низ"))
    li_fig.update_xaxes(title_text="Секунды")
    li_fig.update_yaxes(title_text="% освещёности")

    xy_fig = px.scatter(x=x_data, y=y_data, title="Положение панельки по двум осям")

    temp_fig = make_subplots(rows=2, cols=2,
                               specs=[[{"rowspan": 2}, {}],
                                    [None, {}]],subplot_titles=["График только теператур",
                                                                "Температура + мощность панелек с линзами",
                                                                "Температура + мощность панелек без линз"])

    temp_fig.add_trace(go.Scatter(x=time_start_data, y=temp_lenses, name="С линзами"))
    temp_fig.add_trace(go.Scatter(x=time_start_data, y=temp_standard, name="Без линз"))
    temp_fig.update_xaxes(title_text="Секунды", row=1, col=1)
    temp_fig.update_yaxes(title_text="°C", row=1, col=1)

    temp_fig.add_trace(go.Scatter(x=time_start_data, y=power_lenses_data, name="Мощность"), row=1, col=2)
    temp_fig.add_trace(go.Scatter(x=time_start_data, y=temp_lenses, name="Температура"), row=1, col=2)
    temp_fig.update_xaxes(title_text="Секунды", row=1, col=2)
    temp_fig.update_yaxes(title_text="милиВатты / °C", row=1, col=2)

    temp_fig.add_trace(go.Scatter(x=time_start_data, y=power_standard_data, name="Мощность"), row=2, col=2)
    temp_fig.add_trace(go.Scatter(x=time_start_data, y=temp_lenses, name="Температура"), row=2, col=2)
    temp_fig.update_xaxes(title_text="Секунды", row=2, col=2)
    temp_fig.update_yaxes(title_text="милиВатты / °C", row=2, col=2)

    energy_fig.show()
    li_fig.show()
    xy_fig.show()
    temp_fig.show()

    




# fig = make_subplots(rows=1, cols=2)
# fig.add_trace(go.Scatter(x=[-2, -1, 0, -1, -2], y=[-2, -1, 0, 1, 2]), row=1, col=1)

# fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]), row=1, col=2)

# fig.show()

if __name__ == "__main__":
    qapp = QApplication([])
    window = StartPlotWindow()
    window.show()
    qapp.exec()