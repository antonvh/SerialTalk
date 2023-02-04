## SerialTalk for LPF2

Initial code running on LMS-ESP32 and pybricks (primehub) for showing a proof of concept of bi-directional SerialTalk over the standard LPF2 serial detector protocol.

The library is losely based on the generic SerialTalk library. Because we do not use a serial device having `read`, `write` and `available` methods, we had to adopt the way messages are being received and send ovder the LPF2 connection.

# LMS-ESP32
The LMS-ESP32 emulates a Lego Detector. It creates a mode which allows to receive and send 16 unsigned bytes. 

# pybricks
On the pybricks, the same serialtalk_lpf2 library is running. Here we use the `PUPDevice` class with its `read` and `write` methods to receve and send 16 bytes chuncks from and to the LMS-ESP32. _

