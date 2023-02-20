from socketcan import *

interface = "vcan0"
s = CanRawSocket(interface=interface)

f = open("00x.txt")
for x in f:
  
  can_id = int(x[24:26] + "" + x[27:29],16)
  data = bytes.fromhex(x[0:24])
  
  frame1 = CanFrame(can_id=can_id, data=data)

  s.send(frame1)
