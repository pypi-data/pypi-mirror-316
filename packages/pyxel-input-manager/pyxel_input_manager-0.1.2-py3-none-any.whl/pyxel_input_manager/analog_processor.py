from typing import Dict, Union, Tuple, Protocol, runtime_checkable
from .input_bindings import AnalogBinding, Stick2DBinding, InputBindingBase

@runtime_checkable
class IAnalogProcessor(Protocol):
    """Interface for analog input processing."""

    def process_binding(self, binding: InputBindingBase) -> Union[float, Tuple[float, float]]: ...
    def get_default_value(self, binding: InputBindingBase) -> Union[float, Tuple[float, float]]: ...

class AnalogProcessor(IAnalogProcessor):
    """Processes analog input values."""

    def __init__(self):
        self._analog_cache: Dict[str, Union[float, Tuple[float, float]]] = {}

    def process_binding(self, binding: InputBindingBase) -> Union[float, Tuple[float, float]]:
        """Process an analog binding."""
        return binding.process_input()

    def get_default_value(self, binding: InputBindingBase) -> Union[float, Tuple[float, float]]:
        """Get the default value for an analog binding type."""
        return (0.0, 0.0) if isinstance(binding, Stick2DBinding) else 0.0
