from typing import Dict, List, Optional, Union, overload
from .input_types import InputType
from .input_bindings import AnalogBinding, Stick2DBinding

class InputMap:
    """Manages key bindings for game actions."""

    def __init__(self, initial_bindings: Optional[Dict[str, Union[List[int], AnalogBinding, Stick2DBinding]]] = None):
        """Initialize the InputMap with optional initial bindings.

        Args:
            initial_bindings: Dictionary mapping action names to either:
                            - List[int]: Digital key codes
                            - AnalogBinding: Analog input configuration
                            - Stick2DBinding: 2D stick input configuration
        """
        self._bindings: Dict[str, Union[List[int], AnalogBinding, Stick2DBinding]] = {}
        self._input_types: Dict[str, InputType] = {}

        if initial_bindings:
            for action, binding in initial_bindings.items():
                if isinstance(binding, (AnalogBinding, Stick2DBinding)):
                    self._bindings[action] = binding
                    self._input_types[action] = InputType.ANALOG
                else:
                    self._bindings[action] = binding
                    self._input_types[action] = InputType.DIGITAL

    def add_action(self, action: str, bindings: List[int]) -> bool:
        """Add a new action with its key bindings."""
        if action in self._bindings:
            return False
        self._bindings[action] = bindings.copy()
        self._input_types[action] = InputType.DIGITAL
        return True

    def add_analog_action(self, action: str, binding: AnalogBinding) -> bool:
        """Add a new analog action."""
        if action in self._bindings:
            return False
        self._bindings[action] = binding
        self._input_types[action] = InputType.ANALOG
        return True

    def add_stick2d_action(self, action: str, binding: Stick2DBinding) -> bool:
        """Add a new 2D stick action.

        Args:
            action: The action identifier.
            binding: The Stick2DBinding configuration.

        Returns:
            bool: True if the action was added successfully, False if it already exists.
        """
        if action in self._bindings:
            return False
        self._bindings[action] = binding
        self._input_types[action] = InputType.ANALOG
        return True

    def remove_action(self, action: str) -> bool:
        """Remove an action and its bindings."""
        if action not in self._bindings:
            return False
        del self._bindings[action]
        del self._input_types[action]
        return True

    @overload
    def get_bindings(self, action: str) -> List[int]: ...
    @overload
    def get_bindings(self, action: str) -> AnalogBinding: ...
    @overload
    def get_bindings(self, action: str) -> Stick2DBinding: ...

    def get_bindings(self, action: str) -> Union[List[int], AnalogBinding, Stick2DBinding]:
        """Get the key bindings for an action.

        Args:
            action: The action identifier.

        Returns:
            Union[List[int], AnalogBinding, Stick2DBinding]: The bindings for the action.

        Raises:
            KeyError: If the action doesn't exist.
        """
        if action not in self._bindings:
            raise KeyError(f"Action '{action}' not found")
        return self._bindings[action]

    def set_bindings(self, action: str, bindings: List[int]) -> bool:
        """Set key bindings for an action."""
        if action not in self._bindings:
            return False
        self._bindings[action] = bindings.copy()
        self._input_types[action] = InputType.DIGITAL
        return True

    def has_action(self, action: str) -> bool:
        """Check if an action exists."""
        return action in self._bindings

    def clear_bindings(self):
        """Clear all action bindings."""
        self._bindings.clear()
        self._input_types.clear()

    def get_input_type(self, action: str) -> Optional[InputType]:
        """Get the input type for an action."""
        return self._input_types.get(action)

    def get_all_bindings(self) -> Dict[str, Union[List[int], AnalogBinding, Stick2DBinding]]:
        """Return a dictionary containing all action bindings."""
        return self._bindings

    def validate_action_name(self, action: str) -> None:
        """Validate action name format.

        Args:
            action: The action name to validate.

        Raises:
            ValueError: If the action name is invalid.
        """
        if not action or not action.strip():
            raise ValueError("Action name cannot be empty")
        if not action.isidentifier():
            raise ValueError("Action name must be a valid identifier")

    @property
    def actions(self) -> List[str]:
        """Get list of all registered actions."""
        return list(self._bindings.keys())
