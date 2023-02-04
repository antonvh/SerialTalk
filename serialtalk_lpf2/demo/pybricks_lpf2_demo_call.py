from pybricks.hubs import InventorHub
hub = InventorHub()
s=SerialTalk(Port.F)

while (1):
    ack,val=s.call('joy')
    if ack==b'joya':
        x,y,p=val
        hub.display.off()
        hub.display.pixel(x//50,y//50,100)
        wait(20)