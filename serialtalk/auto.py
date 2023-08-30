from .serialtalk import SerialTalk
import sys

class SerialTalk(SerialTalk):
    """
    SerialTalk class that automatically detects the platform and uses the correct SerialTalk implementation
    also sets the correct default values for the platform.
    """
    def __init__(self, *args, **kwargs):
        _platform = sys.platform

        if _platform == 'esp8266':
            from .esp8266 import Esp8266UART
            super().__init__(Esp8266UART(**kwargs), **kwargs)
        elif _platform == 'esp32':
            from .esp32 import Esp32UART
            super().__init__(Esp32UART(**kwargs), **kwargs)
        elif sys.implementation.name == 'pybricks-micropython': # Pybricks on EV3
            from .pybricks import PBSerial
            super().__init__(PBSerial(*args, **kwargs), **kwargs)
        elif _platform == 'LEGO Learning System Hub':
            from .mshub import MSHubSerial
            super().__init__(MSHubSerial(*args, **kwargs), **kwargs)
        elif 'OpenMV' in _platform:
            from .openmv import OpenMvSerial
            super().__init__(OpenMvSerial(**kwargs), **kwargs)
        elif _platform == 'MaixPy':
            from .k210 import K210Serial
            super().__init__(K210Serial(**kwargs), **kwargs)
        elif sys.implementation.name == 'cpython': # Regular python3
            from .py3 import Py3Serial
            super().__init__(Py3Serial(**kwargs), **kwargs)
        else:
            raise RuntimeError("Platform not supported")
