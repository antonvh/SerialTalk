from pybricks.hubs import InventorHub
hub = InventorHub()
s=SerialTalk(Port.F,name="T\x00\90\x00\x00\x00\x00\x00")

while (1):
    ack,val=s.call('joy')
    if ack==b'joya':
        x,y,p=val
        hub.display.off()
        hub.display.pixel(x//50,y//50,100)
        wait(20)