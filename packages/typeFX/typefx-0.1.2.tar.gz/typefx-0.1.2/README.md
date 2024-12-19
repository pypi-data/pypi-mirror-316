# typeFX

A Python package that creates a typing effect with sound. It uses Pygame to play a sound effect each time a key is typed.

## Installation

You can install the package using pip:

```bash
pip install typeFX
```

Here is an example use of the package:

```python
import pygame
import typeFX as tfx  # Import the typeFX package

# Call the typing_effect function from the package
tfx.type("Hello, World")