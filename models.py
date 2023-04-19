from enum import Enum

from pydantic import BaseModel


class BasePanelData(BaseModel):
    voltage: float
    amperage: float
    temperature: float


class LensesPanel(BasePanelData):
    x: int
    y: int


class LightIntensity(BaseModel):
    top_left: float
    bottom_left: float
    top_right: float
    bottom_right: float


class MainValidator(BaseModel):
    time: int
    number_message: int
    lenses_panels: LensesPanel
    standard_panels: BasePanelData
    light_intensity: LightIntensity
