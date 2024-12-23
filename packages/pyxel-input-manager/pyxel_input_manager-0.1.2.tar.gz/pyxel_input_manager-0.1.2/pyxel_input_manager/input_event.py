import pyxel
from typing import Dict, Union, Tuple
from .input_map import InputMap
from .input_bindings import InputBindingBase
from .state_manager import IStateManager, StateManager
from .analog_processor import IAnalogProcessor, AnalogProcessor

class InputEvent:
    """Manages input states and events."""

    def __init__(self,
                 input_map: InputMap,
                 state_manager: IStateManager = None,
                 analog_processor: IAnalogProcessor = None):
        """Initialize the InputEventManager.

        Args:
            input_map: InputMap instance containing key bindings.
            state_manager: Optional custom state manager implementation.
            analog_processor: Optional custom analog processor implementation.
        """
        if not isinstance(input_map, InputMap):
            raise TypeError("input_map must be an instance of InputMap")

        self._input_map = input_map
        self._state_manager = state_manager or StateManager(list(input_map.get_all_bindings().keys()))
        self._analog_processor = analog_processor or AnalogProcessor()

    def update_states(self) -> None:
        """Updates the current states of all input bindings."""
        for action, binding in self._input_map.get_all_bindings().items():
            if isinstance(binding, InputBindingBase):
                value = self._analog_processor.process_binding(binding)
                self._state_manager.update_state(action, bool(value))
            else:
                # For digital inputs (sequence of key codes)
                is_pressed = any(pyxel.btn(key) for key in binding)
                self._state_manager.update_state(action, is_pressed)

    def is_action_pressed(self, action: str) -> bool:
        """Check if an action is currently being held."""
        return self._state_manager.is_pressed(action)

    def is_action_just_pressed(self, action: str) -> bool:
        """Check if an action was just pressed this frame."""
        return self._state_manager.is_just_pressed(action)

    def is_action_just_released(self, action: str) -> bool:
        """Check if an action was just released this frame."""
        return self._state_manager.is_just_released(action)

    def get_analog_value(self, action: str) -> Union[float, Tuple[float, float]]:
        """Get the current analog value for an action."""
        if not self._input_map.has_action(action):
            raise KeyError(f"Action '{action}' not found in input map")

        binding = self._input_map.get_bindings(action)
        if isinstance(binding, InputBindingBase):
            return self._analog_processor.process_binding(binding)
        return self._analog_processor.get_default_value(binding)

    def reset_states(self) -> None:
        """Reset all input states."""
        self._state_manager.reset()

    def get_value(self, action: str) -> Union[bool, float, Tuple[float, float]]:
        """Gets the current value of an input action."""
        binding = self._input_map.get_bindings(action)
        if isinstance(binding, InputBindingBase):
            return self.get_analog_value(action)
        return self._state_manager.is_pressed(action)
