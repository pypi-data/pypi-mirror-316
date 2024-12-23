import pyxel
from pyxel_input_manager import InputMap, InputEvent, AnalogBinding, Stick2DBinding
from collections import deque
from math import cos, sin, pi

class StickVisualizer:
    """Visualizes analog stick input."""

    def __init__(self, x: int, y: int, label: str):
        """Initialize stick visualizer.

        Args:
            x: X position on screen
            y: Y position on screen
            label: Label text to display
        """
        self.x = x
        self.y = y
        self.label = label
        self.radius = 20
        self.dot_size = 4
        # Store last 10 positions for trail
        self.trail = deque(maxlen=10)

    def draw(self, x_value: float, y_value: float):
        """Draw the stick visualization.

        Args:
            x_value: Horizontal stick position (-1.0 to 1.0)
            y_value: Vertical stick position (-1.0 to 1.0)
        """
        center_x = self.x + self.radius
        center_y = self.y + self.radius

        # Calculate magnitude
        magnitude = min(1.0, (x_value * x_value + y_value * y_value) ** 0.5)

        # Draw outer circle
        pyxel.circb(center_x, center_y, self.radius, 7)

        # Draw crosshair
        pyxel.line(center_x - self.radius, center_y, center_x + self.radius, center_y, 13)
        pyxel.line(center_x, center_y - self.radius, center_x, center_y + self.radius, 13)

        # Calculate stick position
        stick_x = center_x + int(x_value * (self.radius - self.dot_size // 2))
        stick_y = center_y + int(y_value * (self.radius - self.dot_size // 2))

        # Update and draw trail
        self.trail.append((stick_x, stick_y))
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)  # Fade effect
            size = max(1, int(self.dot_size * alpha))
            color = 5 if i < len(self.trail) - 1 else 11  # Last dot is brighter
            pyxel.rect(trail_x - size//2, trail_y - size//2, size, size, color)

        # Draw label
        pyxel.text(self.x, self.y - 8, self.label, 7)

        # Draw magnitude value
        magnitude_text = f"{magnitude:.2f}"
        pyxel.text(self.x, self.y + self.radius * 2 + 4, magnitude_text, 7)

class TriggerVisualizer:
    """Visualizes analog trigger input."""

    def __init__(self, x: int, y: int, label: str):
        """Initialize trigger visualizer.

        Args:
            x: X position on screen
            y: Y position on screen
            label: Label text to display
        """
        self.x = x
        self.y = y
        self.label = label
        self.width = 20
        self.height = 40

    def draw(self, value: float):
        """Draw the trigger visualization.

        Args:
            value: Trigger value (0.0 to 1.0)
        """
        # Draw border
        pyxel.rectb(self.x, self.y, self.width, self.height, 7)

        # Draw fill
        fill_height = int(value * self.height)
        if fill_height > 0:
            pyxel.rect(self.x, self.y + self.height - fill_height,
                      self.width, fill_height, 11)

        # Draw label
        pyxel.text(self.x, self.y - 8, self.label, 7)

def AnalogDemo():
    """Run the input visualization demo."""
    pyxel.init(160, 120, title="Pyxel Input Manager Demo")

    # Create input map with 2D stick bindings
    input_map = InputMap({
        "ls": Stick2DBinding(
            x_axis_code=pyxel.GAMEPAD1_AXIS_LEFTX,
            y_axis_code=pyxel.GAMEPAD1_AXIS_LEFTY
        ),
        "rs": Stick2DBinding(
            x_axis_code=pyxel.GAMEPAD1_AXIS_RIGHTX,
            y_axis_code=pyxel.GAMEPAD1_AXIS_RIGHTY
        ),
        "lt": AnalogBinding(pyxel.GAMEPAD1_AXIS_TRIGGERLEFT),
        "rt": AnalogBinding(pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT),
        "quit": [
            pyxel.KEY_Q,
            pyxel.GAMEPAD1_BUTTON_START
        ],
        "toggle_deadzone": [pyxel.GAMEPAD1_BUTTON_BACK]
    })

    input_event = InputEvent(input_map)

    # Create visualizers
    left_stick = StickVisualizer(20, 12, "Left Stick")
    right_stick = StickVisualizer(90, 12, "Right Stick")
    left_trigger = TriggerVisualizer(50, 62, "LT")
    right_trigger = TriggerVisualizer(120, 62, "RT")

    deadzone = 0.2
    stick_bindings = [
        input_map.get_bindings("ls"),
        input_map.get_bindings("rs")
    ]
    trigger_bindings = [
        input_map.get_bindings("lt"),
        input_map.get_bindings("rt")
    ]

    def update():
        input_event.update_states()

        nonlocal deadzone
        if input_event.is_action_just_pressed("toggle_deadzone"):
            # Cycle through different deadzone values
            deadzone = (deadzone + 0.2) % 1.0  # 0.0 -> 0.2 -> 0.4 -> 0.6 -> 0.8 -> 0.0

            # Update deadzone for all analog inputs
            for binding in stick_bindings + trigger_bindings:
                binding.dead_zone = deadzone

        if input_event.is_action_pressed("quit"):
            pyxel.quit()

    def draw():
        pyxel.cls(0)

        # Get stick values
        ls_x, ls_y = input_event.get_analog_value("ls")
        rs_x, rs_y = input_event.get_analog_value("rs")

        # Draw stick visualizations with the new values
        left_stick.draw(ls_x, ls_y)
        right_stick.draw(rs_x, rs_y)

        # Draw trigger visualizations
        left_trigger.draw(max(0.0, input_event.get_analog_value("lt")))
        right_trigger.draw(max(0.0, input_event.get_analog_value("rt")))

        # Draw instructions
        pyxel.text(2, 112, "Q/START:Quit BACK:Toggle Deadzone", 7)

        # Display current deadzone value
        pyxel.text(2, 104, f"Deadzone: {deadzone:.1f}", 7)

    pyxel.run(update, draw)

def main():
    """Entry point for the CLI."""
    AnalogDemo()

if __name__ == "__main__":
    main()
