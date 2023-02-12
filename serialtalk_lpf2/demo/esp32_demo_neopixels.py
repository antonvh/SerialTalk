from serialtalk_lpf2 import *
from time import sleep_ms
from machine import Pin
from neopixel import NeoPixel

np=NeoPixel(Pin(21),64)

last=[]

def led(nr):
    global last
    print(nr)
    last.append(nr)
    last=last[-20:]
    for i,nri in enumerate(last):
        b=int(i*2)
        #print(nr,b)
        np[nri]=(b,b,b)
    show()
    
def show():
    np.write()


def wipe():
    np.fill((0,0,0))
    np.write()
    
s=SerialTalk(1,power_motor=True) # enable external power
s.add_command(led)
s.add_command(show)
s.add_command(wipe)

while True:
    if not s.lpf2.connected:
        print("reconnecting lpf2")
        s.lpf2.sendTimer.deinit()
        #led.on()
        sleep_ms(200)
        s.lpf2.baud=2400
        s.lpf2.initialize()
    sleep_ms(200)
 
