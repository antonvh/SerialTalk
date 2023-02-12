from pybricks.hubs import InventorHub
hub = InventorHub()
s=SerialTalk(Port.A)
last=[]
s.send_command('wipe')
while(1):
    h,v=hub.imu.tilt()
    v=((v+50)//12)%8
    h=((h+50)//12)%8
    nr=v*8+h
    s.send_command('led','B',nr)
    wait(50)