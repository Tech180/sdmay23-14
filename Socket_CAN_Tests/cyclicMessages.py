from socketcan import *


interface = "vcan0"
s = CanBcmSocket(interface=interface)

can_id = 0x12345678
data = bytes(range(0, 0x88, 0x11))
frame = CanFrame(can_id=can_id,
                  data=data)
opcode = BcmOpCodes.TX_SETUP
flags = BCMFlags.SETTIMER | BCMFlags.STARTTIMER
interval = 1
frames = [frame, ]
bcm = BcmMsg(opcode=opcode,
             flags=flags,
             count=0,
             interval1=0,
             interval2=interval,
             can_id=can_id,
             frames=frames
             )
s.send(bcm)

sleep(10)
