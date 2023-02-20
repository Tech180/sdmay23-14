from socketcan import *

interface = "vcan0"
s = CanRawSocket(interface=interface)

f = open("sample-can.log")
for x in f:
  idString = x[0:3]
  dataString = x[4:]
  
  can_id = int(idString,16)
  data = bytes.fromhex(dataString)
  
  frame1 = CanFrame(can_id=can_id, data=data)

  s.send(frame1)
