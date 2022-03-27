# SerialTalk: platform independent symmetric communication library
## Goal
The goal of the package is to facilitate communication between devices like Robots and peripheral embedded systems or monitors over a serial communication line. Sounds abstract? Think connecting an OpenMV camera to a LEGO SPIKE Prime Robot. Or linking up two pyboards. 

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

## Roadmap, todo
- test on esp8266 platform
- test on bt comm channels
- create pyserial/desktop channels 
