from serialtalk_lpf2 import *
from time import sleep_ms

def add(a,b):
    print(s.rcv_ctr)
    return a+b

def check(a):
    print(a)


from machine import I2C, Pin

i2c = I2C(1,sda=Pin(5),scl=Pin(4))
i2c.scan()

def joy():
    x,y,p=i2c.readfrom(82,3)
    return x,y,p


s=SerialTalk(1)

while(1):
    x,y,p=joy()
    s.send_command('joy','3B',x,y,p)
    sleep_ms(20)