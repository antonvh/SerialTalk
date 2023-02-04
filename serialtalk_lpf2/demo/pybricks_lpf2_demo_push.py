from pybricks.hubs import InventorHub
hub = InventorHub()
s=SerialTalk(Port.F)
lastpixel=[]
while (1):

    cmd,val=s.receive_command(reset_rcv_ctr=True)
    if cmd==b'joy':
        x,y,p=val
        hub.display.off()
        xx=x//50
        yy=y//50
        lastpixel.append([x,y])
        lastpixel=lastpixel[-10:]
        for i,xy in enumerate(lastpixel):
            x,y=xy
            hub.display.pixel(x//50,y//50,i*10)
        wait(50)
    