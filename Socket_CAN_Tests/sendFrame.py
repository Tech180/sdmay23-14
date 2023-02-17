from socketcan import CanRawSocket, CanFrame

interface = "vcan0"
s = CanRawSocket(interface=interface)

can_id = 0x123456
data = bytes(range(0,0x86,0x12))
frame1 = CanFrame(can_id=can_id, data=data)

s.send(frame1)
