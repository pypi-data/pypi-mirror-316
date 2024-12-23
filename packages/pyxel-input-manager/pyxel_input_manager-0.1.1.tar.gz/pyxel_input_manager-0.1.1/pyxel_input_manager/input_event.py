import pyxel
from typing import Dict, Union, Sequence, Tuple, Optional, NoReturn
from .input_types import InputType
from .input_map import InputMap
from .input_bindings import AnalogBinding, Stick2DBinding

class InputEvent:
    """Manages input states and events."""

    def __init__(self, input_map: InputMap):
        """Initialize the InputEventManager.

        Args:
            input_map (InputMap): InputMap instance containing key bindings.
        """
        if not isinstance(input_map, InputMap):
            raise TypeError("input_map must be an instance of InputMap")
        self._input_map = input_map
        all_actions = self._input_map.get_all_bindings().keys()
        self._previous_states = {k: False for k in all_actions}
        self._current_states = {k: False for k in all_actions}
        self._analog_values = {}

    def update_states(self) -> None:
        """Updates the current states of all input bindings."""
        self._previous_states = self._current_states.copy()

        for action, binding in self._input_map.get_all_bindings().items():
            if isinstance(binding, (AnalogBinding, Stick2DBinding)):
                self._current_states[action] = binding.process_input()
            else:
                # For digital inputs (sequence of key codes)
                self._current_states[action] = any(pyxel.btn(key) for key in binding)

    def is_action_pressed(self, action: str) -> bool:
        """Check if an action is currently being held."""
        return self._current_states.get(action, False)

    def is_action_just_pressed(self, action: str) -> bool:
        """Check if an action was just pressed this frame."""
        return (self._current_states.get(action, False) and
                not self._previous_states.get(action, False))

    def is_action_just_released(self, action: str) -> bool:
        """Check if an action was just released this frame."""
        return (not self._current_states.get(action, False) and
                self._previous_states.get(action, False))

    def get_analog_value(self, action: str) -> Union[float, Tuple[float, float]]:
        """Get the current analog value for an action.

        Args:
            action: The action identifier.

        Returns:
            Union[float, Tuple[float, float]]: The analog value(s).

        Raises:
            KeyError: If the action doesn't exist.
        """
        if not self._input_map.has_action(action):
            raise KeyError(f"Action '{action}' not found in input map")
        value = self._current_states.get(action)
        binding = self._input_map.get_bindings(action)

        if isinstance(binding, Stick2DBinding):
            if isinstance(value, tuple):
                return value
            return (0.0, 0.0)
        elif isinstance(binding, AnalogBinding):
            if isinstance(value, (int, float)):
                return float(value)
            return 0.0

        return 0.0

    def reset_states(self) -> None:
        """Reset all input states."""
        all_actions = self._input_map.get_all_bindings().keys()
        self._previous_states = {k: False for k in all_actions}
        self._current_states = {k: False for k in all_actions}
        self._analog_values.clear()

    def get_value(self, action: str) -> Union[bool, float, Tuple[float, float]]:
        """Gets the current value of an input action.

        Args:
            action: The action identifier.

        Returns:
            Union[bool, float, Tuple[float, float]]: The current state of the input.
            - bool for digital inputs
            - float for AnalogBinding
            - Tuple[float, float] for Stick2DBinding
        """
        binding = self._input_map.get_bindings(action)
        if isinstance(binding, (AnalogBinding, Stick2DBinding)):
            return self._current_states.get(action, 0.0 if isinstance(binding, AnalogBinding) else (0.0, 0.0))
        return bool(self._current_states.get(action, False))

    def _cache_analog_values(self) -> None:
        """Cache analog values for performance optimization."""
        self._analog_cache = {}
        for action, binding in self._input_map.get_all_bindings().items():
            if isinstance(binding, (AnalogBinding, Stick2DBinding)):
                self._analog_cache[action] = binding.process_input()
