import pyxel
from pyxel_input_manager import InputMap, InputEvent, AnalogBinding, Stick2DBinding

import math

class InputDemo:
    """Simple demo showing input manager usage."""

    def __init__(self):
        """Initialize the demo."""
        pyxel.init(160, 144, title="Input Manager Demo")

        # Create player
        self.player_x = 80
        self.player_y = 60
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.8
        self.friction = 0.75
        self.max_speed = 2.5

        self.setup_input()
        pyxel.run(self.update, self.draw)

    def setup_input(self):
        """Setup input mapping."""
        initial_bindings = {
            # Digital inputs
            "move_right": [pyxel.KEY_D, pyxel.KEY_RIGHT, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT],
            "move_left": [pyxel.KEY_A, pyxel.KEY_LEFT, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT],
            "move_up": [pyxel.KEY_W, pyxel.KEY_UP, pyxel.GAMEPAD1_BUTTON_DPAD_UP],
            "move_down": [pyxel.KEY_S, pyxel.KEY_DOWN, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN],
            "quit": [
                pyxel.KEY_Q, pyxel.GAMEPAD1_BUTTON_START
            ],

            # 2D Analog stick
            "movement": Stick2DBinding(
                x_axis_code=pyxel.GAMEPAD1_AXIS_LEFTX,
                y_axis_code=pyxel.GAMEPAD1_AXIS_LEFTY,
                dead_zone=0.2
            )
        }

        self.input_map = InputMap(initial_bindings)
        self.input_event = InputEvent(self.input_map)

    def update(self):
        """Update game state."""
        self.input_event.update_states()

        # Check for quit
        if self.input_event.is_action_pressed("quit"):
            pyxel.quit()

        # Calculate input direction
        input_x = 0
        input_y = 0

        # Digital input
        if self.input_event.is_action_pressed("move_right"):
            input_x += 1
        if self.input_event.is_action_pressed("move_left"):
            input_x -= 1
        if self.input_event.is_action_pressed("move_up"):
            input_y -= 1
        if self.input_event.is_action_pressed("move_down"):
            input_y += 1

        # Analog stick input
        stick_x, stick_y = self.input_event.get_analog_value("movement")
        input_x += stick_x
        input_y += stick_y

        # Normalize diagonal movement
        if input_x != 0 and input_y != 0:
            magnitude = (input_x * input_x + input_y * input_y) ** 0.5
            input_x /= magnitude
            input_y /= magnitude

        # Apply acceleration
        self.velocity_x += input_x * self.acceleration
        self.velocity_y += input_y * self.acceleration

        # Apply friction
        if abs(input_x) < 0.1:
            self.velocity_x *= self.friction
        if abs(input_y) < 0.1:
            self.velocity_y *= self.friction

        # Limit maximum speed
        speed = (self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5
        if speed > self.max_speed:
            self.velocity_x = (self.velocity_x / speed) * self.max_speed
            self.velocity_y = (self.velocity_y / speed) * self.max_speed

        # Stop at very low speeds
        if abs(self.velocity_x) < 0.01:
            self.velocity_x = 0
        if abs(self.velocity_y) < 0.01:
            self.velocity_y = 0

        # Update position
        self.player_x += self.velocity_x
        self.player_y += self.velocity_y

        # Keep player in bounds
        self.player_x = max(0, min(pyxel.width - 8, self.player_x))
        self.player_y = max(0, min(pyxel.height - 8, self.player_y))

    def draw(self):
        """Draw game state."""
        pyxel.cls(1)

        # Draw shadow
        pyxel.rect(int(self.player_x) + 2, int(self.player_y) + 2, 8, 8, 5)

        # Draw player
        pyxel.rect(int(self.player_x), int(self.player_y), 8, 8, 11)

        # Draw HUD
        pyxel.text(4, 4, "WASD/Arrows/D-Pad: Move", 7)
        pyxel.text(4, 12, "Left Stick: Move", 7)
        pyxel.text(4, 20, "Q or START: Quit", 7)

        # Draw velocity info
        velocity_str = f"Vel: ({self.velocity_x:.2f}, {self.velocity_y:.2f})"
        speed = (self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5
        speed_str = f"Speed: {speed:.2f}"

        pyxel.text(4, 32, velocity_str, 7)
        pyxel.text(4, 40, speed_str, 7)

def main():
    """Entry point for CLI."""
    InputDemo()

if __name__ == "__main__":
    main()
