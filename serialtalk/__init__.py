#!micropython
"""
SerialTalk - Platform-independent symmetric communication library

This package facilitates communication between devices like Robots and
peripheral embedded systems or monitors over a serial communication line.

Author: Anton Vanhoucke, Ste7an
Copyright: Copyright 2023-2025, AntonsMindstorms.com
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Anton Vanhoucke, Ste7an"
__copyright__ = "Copyright 2023-2025, AntonsMindstorms.com"
__license__ = "MIT"
__status__ = "Production"
__email__ = "anton@antonsmindstorms.com"
__url__ = "https://github.com/antonvh/SerialTalk"

# Submodules contain serial wrappers around common communication channels.
# All classes support read, write, any
# To support REPL they need to have a port property.

# Import main module:
from .serialtalk import SerialTalk

__all__ = ["SerialTalk"]
