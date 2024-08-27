# Upload this file to LMS-ESP32 v2.0

from neopixel import NeoPixel
from machine import Pin
from np_animation import hsl_to_rgb
from time import sleep_ms
from serialtalk.auto import SerialTalk

np = NeoPixel(Pin(25), 1)
st = SerialTalk(rx_pin=22, tx_pin=21)

def led(hue):
    np[0] = hsl_to_rgb(hue, 100, 30)
    np.write()
    
st.add_command(led)

while 1:
    st.process()