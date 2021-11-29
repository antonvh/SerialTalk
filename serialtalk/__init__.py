#!micropython

# Submodules contain serial wrappers around common communication channels.
# All classes support read, write, any
# To support REPL they need to have a port property.

# Import main module:
from .serialtalk import SerialTalk