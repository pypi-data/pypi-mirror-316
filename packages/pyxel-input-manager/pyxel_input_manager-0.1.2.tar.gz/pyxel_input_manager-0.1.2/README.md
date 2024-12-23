# Pyxel Input Manager

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/pyxel-input-manager.svg)](https://badge.fury.io/py/pyxel-input-manager)

A flexible and easy-to-use input management system for the [Pyxel](https://github.com/kitao/pyxel) retro game engine.

## Features

- 🎮 Comprehensive input support
  - Digital inputs (keyboard, gamepad buttons)
  - Analog inputs (gamepad axes)
  - 2D stick inputs with proper dead zone handling
- 🎯 Action-based input mapping
- 🔄 Runtime rebinding support
- ⚡ Efficient state management
- 🛠️ Dead zone configuration
- 📦 Zero external dependencies (other than Pyxel)

## Installation

```sh
pip install pyxel-input-manager
```

Requires Python 3.11 or higher and Pyxel.

## Quick Start

```python
import pyxel
from pyxel_input_manager import InputMap, InputEvent, AnalogBinding, Stick2DBinding

class Game:
    def __init__(self):
        pyxel.init(160, 120)

        # Setup input mapping
        self.input_map = InputMap({
            "move_right": [pyxel.KEY_RIGHT, pyxel.KEY_D],  # Multiple keys
            "jump": [pyxel.KEY_SPACE],
            "analog_move": Stick2DBinding(  # 2D analog stick
                pyxel.GAMEPAD1_AXIS_LEFTX,
                pyxel.GAMEPAD1_AXIS_LEFTY,
                dead_zone=0.2
            )
        })

        self.input_event = InputEvent(self.input_map)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.input_event.update_states()

        # Digital input example
        if self.input_event.is_action_pressed("move_right"):
            self.player_x += 1

        # Analog input example
        x, y = self.input_event.get_analog_value("analog_move")
        self.player_x += x * 2
        self.player_y += y * 2

    def draw(self):
        pyxel.cls(0)
```

## Advanced Usage

### Adding Actions at Runtime

```python
input_map.add_action("attack", [pyxel.KEY_Z])
input_map.add_analog_action("aim", AnalogBinding(
    pyxel.GAMEPAD1_AXIS_RIGHTX,
    dead_zone=0.1,
    invert=False
))
```

### Input State Checks

```python
# Just pressed this frame
if input_event.is_action_just_pressed("jump"):
    player.jump()

# Continuously held
if input_event.is_action_pressed("run"):
    player.run()

# Just released this frame
if input_event.is_action_just_released("charge"):
    player.release_charge()
```

### Analog Input Processing

```python
# Get analog value
throttle = input_event.get_analog_value("throttle")

# Get 2D stick input
x, y = input_event.get_analog_value("move_stick")
```

For detailed API documentation, see [API Reference](docs/api_reference.md).

## Development

<!-- ### Running Tests

```sh
python -m pytest tests/
``` -->

### Running Demo

```sh
python -m pyxel_input_manager demo
python -m pyxel_input_manager demo_analog  # Analog input demo
```

<!-- ## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Pyxel](https://github.com/kitao/pyxel) - The retro game engine this library is built for
