import pyxel
from abc import ABC, abstractmethod
from math import sqrt
from typing import Final, Union, Tuple, ClassVar

class InputBindingBase(ABC):
    """Abstract base class for input bindings."""

    MAX_VALUE: ClassVar[float] = 32767.0

    def __init__(self, dead_zone: float = 0.2):
        """Initialize base input binding.

        Args:
            dead_zone: Dead zone threshold, defaults to 0.2 (20%).
        """
        self.dead_zone = dead_zone

    @property
    def dead_zone(self) -> float:
        """Get the dead zone value."""
        return self._dead_zone

    @dead_zone.setter
    def dead_zone(self, value: float) -> None:
        """Set the dead zone value with validation."""
        if not 0.0 <= value <= 1.0:
            raise ValueError("dead_zone must be between 0.0 and 1.0")
        self._dead_zone = value

    def _normalize_input(self, raw_value: float) -> float:
        """Normalize raw input value to range -1.0 to 1.0."""
        return raw_value / self.MAX_VALUE

    def _apply_dead_zone(self, value: float) -> float:
        """Apply dead zone processing to a normalized value."""
        abs_val = abs(value)
        if abs_val < self.dead_zone:
            scaled = (abs_val / self.dead_zone) * abs_val
        else:
            scaled = (abs_val - self.dead_zone) / (1.0 - self.dead_zone)
            scaled = max(0.0, min(1.0, scaled))
        return scaled * (1 if value >= 0 else -1)

    @abstractmethod
    def process_input(self) -> Union[float, Tuple[float, float]]:
        """Process the input and return the processed value(s)."""
        pass

class AnalogBinding(InputBindingBase):
    """Manages analog input binding configuration."""

    def __init__(self, axis_code: int, dead_zone: float = 0.2, invert: bool = False):
        """Initialize analog binding."""
        super().__init__(dead_zone)
        if not isinstance(axis_code, int):
            raise TypeError("axis_code must be an integer")
        self.axis_code = axis_code
        self.invert = invert

    def process_input(self) -> float:
        """Process the analog input with a dead zone and optional inversion."""
        raw_value = self._normalize_input(pyxel.btnv(self.axis_code))
        value = self._apply_dead_zone(raw_value)
        return -value if self.invert else value

class Stick2DBinding(InputBindingBase):
    """Manages 2D analog stick input binding configuration."""

    def __init__(self, x_axis_code: int, y_axis_code: int,
                 dead_zone: float = 0.2,
                 invert_x: bool = False, invert_y: bool = False):
        """Initialize 2D stick binding."""
        super().__init__(dead_zone)
        if not all(isinstance(code, int) for code in (x_axis_code, y_axis_code)):
            raise TypeError("Axis codes must be integers")
        self.x_axis_code = x_axis_code
        self.y_axis_code = y_axis_code
        self.invert_x = invert_x
        self.invert_y = invert_y

    def process_input(self) -> tuple[float, float]:
        """Process the 2D analog stick input with a smoother radial dead zone."""
        raw_x = self._normalize_input(pyxel.btnv(self.x_axis_code))
        raw_y = self._normalize_input(pyxel.btnv(self.y_axis_code))
        magnitude = sqrt(raw_x * raw_x + raw_y * raw_y)

        if magnitude < self.dead_zone or magnitude == 0:
            return 0.0, 0.0

        norm_x = raw_x / magnitude
        norm_y = raw_y / magnitude
        scaled_mag = min(1.0, (magnitude - self.dead_zone) / (1.0 - self.dead_zone))

        final_x = norm_x * scaled_mag
        final_y = norm_y * scaled_mag

        return (
            -final_x if self.invert_x else final_x,
            -final_y if self.invert_y else final_y
        )
