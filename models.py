from enum import Enum
from pydantic import BaseModel


class BasePanelData(BaseModel):
    voltage: float
    amperage: float


class LensesPanel(BasePanelData):
    voltage: float
    amperage: float


class CurrentActionEnum(str, Enum):
    move_x = "move_x"
    move_y = "move_y"
    wait_changes = "wait_changes"


class LightIntensity(BaseModel):
    top: float
    bottom: float
    left: float
    right: float


class MainValidator(BaseModel):
    time: int
    currect_action: CurrentActionEnum
    lenses_panels: LensesPanel
    standard_panels: BasePanelData
    light_intensity: LightIntensity
