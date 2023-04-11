from typing import List, Optional, Union
from enum import Enum

class SequenceType(str, Enum):
    """Enumeration of sequence types."""
    CURRENT = "current"
    VOLTAGE = "voltage"
    POWER = "power"
    DURATION = "duration"
    HPPC = "HPPC"
    CCCV = "CCCV"
    REST = "rest"

class TerminationType(str, Enum):
    """Enumeration of termination types."""
    CURRENT = "current"
    VOLTAGE = "voltage"
    POWER = "power"
    DURATION = "duration"
    TEMPERATURE = "temperature"

class ExperimentConfig:
    """Class to store the global configuration settings for an experiment."""
    def __init__(self, V_unit: str, C_unit: str, T_unit: str, duration_unit: str, V_min: float, V_max: float, T_ambient: int, T_max: int):
        self.V_unit = V_unit
        self.C_unit = C_unit
        self.T_unit = T_unit
        self.duration_unit = duration_unit
        self.V_min = V_min
        self.V_max = V_max
        self.T_ambient = T_ambient
        self.T_max = T_max

    def to_dict(self) -> dict:
        return {
            'V_unit': self.V_unit,
            'C_unit': self.C_unit,
            'T_unit': self.T_unit,
            'duration_unit': self.duration_unit,
            'V_min': self.V_min,
            'V_max': self.V_max,
            'T_ambient': self.T_ambient,
            'T_max': self.T_max,
        }

class TerminationCondition:
    """Class to store termination conditions."""
    def __init__(self, type: TerminationType, value: float, name: Optional[str] = None):
        self.type = type
        self.value = value
        self.name = name

    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'value': self.value,
            'name': self.name,
        }

class Instruction:
    """Class to store an instruction."""
    def __init__(
        self,
        type: SequenceType,
        value: Optional[float] = None,
        time: Optional[int] = None,
        termination: Optional[List[TerminationCondition]] = None,
        name: Optional[str] = None,
        repeat: int = 1,
    ):
        self.type = type
        self.value = value
        self.time = time
        self.termination = termination
        self.name = name
        self.repeat = repeat

    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'value': self.value,
            'time': self.time,
            'termination': [t.to_dict() for t in self.termination] if self.termination else None,
            'name': self.name,
            'repeat': self.repeat,
        }


class Sequence:
    """Class to store a sequence of instructions."""
    def __init__(self, sequence: List[Union['Instruction', 'Sequence']], name: Optional[str] = None, repeat: int = 1):
        self.sequence = sequence
        self.name = name
        self.repeat = repeat

    def to_dict(self) -> dict:
        return {
            'sequence': [s.to_dict() for s in self.sequence],
            'name': self.name,
            'repeat': self.repeat,
        }


class CyclerConfig:
    """Class to store the cycler configuration."""
    def __init__(self, globals: ExperimentConfig, instructions: List[Union[Instruction, Sequence]]):
        self.globals = globals
        self.instructions = instructions

    def to_dict(self) -> dict:
        return {
            'globals': self.globals.to_dict(),
            'instructions': [i.to_dict() for i in self.instructions],
        }