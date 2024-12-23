import pyxel
from math import sqrt
from typing import Final

class AnalogBinding:
    """Manages analog input binding configuration.

    Attributes:
        axis_code (int): The pyxel axis code for the analog input.
        dead_zone (float): The dead zone threshold (0.0 to 1.0).
        invert (bool): Whether to invert the input value.
    """
    MAX_VALUE: Final[float] = 32767.0

    def __init__(self, axis_code: int, dead_zone: float = 0.2, invert: bool = False):
        """Initialize analog binding.

        Args:
            axis_code: The pyxel axis code (e.g., GAMEPAD1_AXIS_LEFTX).
            dead_zone: Dead zone threshold, defaults to 0.2 (20%).
            invert: Whether to invert the axis value.
        """
        if not isinstance(axis_code, int):
            raise TypeError("axis_code must be an integer")
        if not 0.0 <= dead_zone <= 1.0:
            raise ValueError("dead_zone must be between 0.0 and 1.0")

        self.axis_code = axis_code
        self.dead_zone = max(0.0, min(1.0, dead_zone))
        self.invert = invert

    @property
    def dead_zone(self) -> float:
        """Get the dead zone value."""
        return self._dead_zone

    @dead_zone.setter
    def dead_zone(self, value: float) -> None:
        """Set the dead zone value with validation."""
        self._dead_zone = max(0.0, min(1.0, value))

    def process_input(self) -> float:
        """Process the analog input with a smoother dead zone and optional inversion.

        Returns:
            float: Processed analog value between -1.0 and 1.0.
        """
        raw_value = pyxel.btnv(self.axis_code) / 32767.0
        abs_val = abs(raw_value)

        if abs_val < self.dead_zone:
            # Interpolate from 0.0 to dead_zone for smoother transitions
            scaled = (abs_val / self.dead_zone) * abs_val
        else:
            scaled = (abs_val - self.dead_zone) / (1.0 - self.dead_zone)
            scaled = max(0.0, min(1.0, scaled))

        value = scaled * (1 if raw_value >= 0 else -1)
        return -value if self.invert else value

class Stick2DBinding:
    """Manages 2D analog stick input binding configuration.

    Attributes:
        x_axis_code (int): The pyxel axis code for X axis.
        y_axis_code (int): The pyxel axis code for Y axis.
        dead_zone (float): The dead zone threshold (0.0 to 1.0).
        invert_x (bool): Whether to invert the X axis value.
        invert_y (bool): Whether to invert the Y axis value.
    """
    MAX_VALUE: Final[float] = 32767.0

    def __init__(self, x_axis_code: int, y_axis_code: int,
                 dead_zone: float = 0.2,
                 invert_x: bool = False, invert_y: bool = False):
        """Initialize 2D stick binding.

        Args:
            x_axis_code: The pyxel axis code for X axis.
            y_axis_code: The pyxel axis code for Y axis.
            dead_zone: Dead zone threshold, defaults to 0.2 (20%).
            invert_x: Whether to invert the X axis value.
            invert_y: Whether to invert the Y axis value.
        """
        if not all(isinstance(code, int) for code in (x_axis_code, y_axis_code)):
            raise TypeError("Axis codes must be integers")

        self.x_axis_code = x_axis_code
        self.y_axis_code = y_axis_code
        self.dead_zone = max(0.0, min(1.0, dead_zone))
        self.invert_x = invert_x
        self.invert_y = invert_y

    def process_input(self) -> tuple[float, float]:
        """Process the 2D analog stick input with a smoother radial dead zone.

        Returns:
            tuple[float, float]: X and Y values, each between -1.0 and 1.0.
        """
        raw_x = pyxel.btnv(self.x_axis_code) / 32767.0
        raw_y = pyxel.btnv(self.y_axis_code) / 32767.0
        magnitude = sqrt(raw_x * raw_x + raw_y * raw_y)

        if magnitude < self.dead_zone:
            return 0.0, 0.0

        # Calculate normalized direction
        norm_x = raw_x / magnitude
        norm_y = raw_y / magnitude

        # Apply scaled magnitude beyond dead zone
        scaled_mag = min(1.0, (magnitude - self.dead_zone) / (1.0 - self.dead_zone))
        final_x = norm_x * scaled_mag
        final_y = norm_y * scaled_mag

        return (
            -final_x if self.invert_x else final_x,
            -final_y if self.invert_y else final_y
        )
