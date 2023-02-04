# SerialTalk for LPF2

Initial code running on LMS-ESP32 and pybricks (primehub) for showing a proof of concept of bi-directional SerialTalk over the standard LPF2 serial detector protocol.

The library is losely based on the generic SerialTalk library. Because we do not use a serial device having `read`, `write` and `available` methods, we had to adopt the way messages are being received and send ovder the LPF2 connection.

## LMS-ESP32
The LMS-ESP32 emulates a Lego Detector. It creates a mode which allows to receive and send 16 unsigned bytes. 

## PyBricks
On the pybricks, the same serialtalk_lpf2 library is running. Here we use the `PUPDevice` class with its `read` and `write` methods to receve and send 16 bytes chuncks from and to the LMS-ESP32.

## Files

`serialtalk_lpf2.py` is the library that runs both on the LMS-ESP32 as well as the PyBricks PrimeHub. On the primehub you have to paste the code of this library (select raw mode) in the editor of PyBricks and append the example code below it. On the ESP32 yoy have to upload this library to the root of the flash filesystem tohether with the `LPF2_ESP32.py` library which is for emulating a native Lego LPF2 sensor.



