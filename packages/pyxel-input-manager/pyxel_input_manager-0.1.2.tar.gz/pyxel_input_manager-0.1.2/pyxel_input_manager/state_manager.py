from typing import Dict, Any, Protocol, runtime_checkable

@runtime_checkable
class IStateManager(Protocol):
    """Interface for state management."""

    def update_state(self, action: str, new_state: bool) -> None: ...
    def is_pressed(self, action: str) -> bool: ...
    def is_just_pressed(self, action: str) -> bool: ...
    def is_just_released(self, action: str) -> bool: ...
    def reset(self) -> None: ...

class StateManager(IStateManager):
    """Manages the state of input actions."""

    def __init__(self, initial_actions: list[str]):
        """Initialize the state manager.

        Args:
            initial_actions: List of action names to initialize states for.
        """
        self._previous_states: Dict[str, bool] = {k: False for k in initial_actions}
        self._current_states: Dict[str, bool] = {k: False for k in initial_actions}

    def update_state(self, action: str, new_state: bool) -> None:
        """Update the state of an action.

        Args:
            action: The action identifier.
            new_state: The new state value.
        """
        self._previous_states[action] = self._current_states[action]
        self._current_states[action] = new_state

    def is_pressed(self, action: str) -> bool:
        """Check if an action is currently pressed."""
        return self._current_states.get(action, False)

    def is_just_pressed(self, action: str) -> bool:
        """Check if an action was just pressed this frame."""
        return (self._current_states.get(action, False) and
                not self._previous_states.get(action, False))

    def is_just_released(self, action: str) -> bool:
        """Check if an action was just released this frame."""
        return (not self._current_states.get(action, False) and
                self._previous_states.get(action, False))

    def reset(self) -> None:
        """Reset all states to default values."""
        for action in self._current_states:
            self._previous_states[action] = False
            self._current_states[action] = False
