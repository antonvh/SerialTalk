<div align="center">
<img alt="rcservo logo" src="https://raw.githubusercontent.com/antonvh/serialtalk/master/images/serialtalk.png" width="200">

# SerialTalk: platform-independent symmetric communication library

This package facilitates communication between devices like Robots and peripheral embedded systems or monitors over a serial communication line. Sounds abstract? Think of connecting an OpenMV camera to a LEGO SPIKE Prime Robot. Or linking up two Pyboards.

[![PyPI version](https://badge.fury.io/py/rcservo.svg)](https://badge.fury.io/py/rcservo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MicroPython Compatible](https://img.shields.io/badge/MicroPython-Compatible-brightgreen.svg)](https://micropython.org/)

</div>

## Installation

### For Python (PyPI)

Install from PyPI using pip:

```bash
pip install serialtalk
```

### For MicroPython

#### Option 1: Using viperIDE.org (Recommended)

1. Go to [viperIDE.org](https://viperide.org)
2. Connect to your MicroPython device
3. Navigate to **Tools** > **Package Manager**
4. Click **Install package via link**
5. Enter: `github:antonvh/SerialTalk`

#### Option 2: Using mpremote

```bash
mpremote mip install github:antonvh/SerialTalk
```

#### Option 3: Using mip from device REPL

```python
import mip
mip.install("github:antonvh/SerialTalk")
```

## Usage

When you want default UART for the platform you're running on, just go:
`from serialtalk.auto import SerialTalk`

When you want special channels like sockets or bluetooth, do it like this:

``` python
from serialtalk import SerialTalk
from serialtalk.sockets import ClientSocketSerial

ser = SerialTalk(ClientSocketSerial("127.0.0.1",8080))
ser.call('echo','read?')
```

## Example with OpenMV H7

1. Copy the complete `serialtalk` directory to the OpenMV flash (not the whole SerialTalk, just the `serialtalk` subfolder)

2. Create a main.py with this code. It is an adaptation of the OpenMV Hello world

   ```python
   import sensor, image, time
   from serialtalk.auto import SerialTalk

   sensor.reset()                      # Reset and initialize the sensor.
   sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
   sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
   sensor.skip_frames(time = 2000)     # Wait for settings take effect.
   clock = time.clock()                # Create a clock object to track the FPS.

   st = SerialTalk()                   # Create UART comm object
   def fps():                          # Create function to call from uart
       return clock.fps()
   st.add_command(fps,"repr")          # Add function to callable uart commands

   while(True):
       clock.tick()                    # Update the FPS clock.
       img = sensor.snapshot()         # Take a picture and return the image.
       st.process_uart()               # Process aurt calls
       print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                       # to the IDE. The FPS should increase once disconnected.
   ```

3. On the SPIKE Prime [Install mpy-robot-tools](https://github.com/antonvh/mpy-robot-tools/blob/master/Installer/install_mpy_robot_tools.py) with the installer script. Note that the installer may seem unresponsive. Just have some patience.

4. Run this script on SPIKE Prime:

   ```python
   from projects.mpy_robot_tools.serialtalk import SerialTalk
   from projects.mpy_robot_tools.mshub import MSHubSerial

   st = SerialTalk(MSHubSerial('F'))

   print(st.call('echo','Hello there OpenMV!'))
   print(st.call('fps'))
   ```

This should be the result:

![Spike result](images/spike_result.png)

## Roadmap, todo

- test on esp8266 platform
- test on bt comm channels
- create pyserial/desktop channels
