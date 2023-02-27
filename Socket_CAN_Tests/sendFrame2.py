
from socketcan import *

interface = "vcan0"
#s = CanRawSocket(interface=interface, fd=True)
s = can.interfaces.socketcan.SocketcanBus(channel="vcan0", fd=True)


f = open("00x2.txt")
for x in f:
  
  can_id = int(x[16:18] + "" + x[18:20] + x[20:22],16)
  data = bytes.fromhex(x[0:16]) + bytes.fromhex(x[0:16]) + bytes.fromhex(x[0:16]) + bytes.fromhex(x[0:16]) + bytes.fromhex(x[0:16])
  
  frame1 = CanFrame(can_id=can_id, data=data)

  s.send(frame1)
