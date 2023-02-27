
import time
import can

bustype = 'socketcan'
channel = 'vcan0'


def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    #bus = can.Bus(channel=channel, interface=bustype)
    bus = can.interfaces.socketcan.SocketcanBus(channel='vcan0', fd=True)
    f = open("00x2.txt")

    for x in f:
        can_id = int(x[16:18] + "" + x[18:20] + x[20:22],16)
        data_msg = [int(x[0:16] + ""), 1, 2, 3]
        msg = can.Message(arbitration_id=can_id, data=data_msg, is_extended_id=False)
        bus.send(msg)

    time.sleep(1)

producer(10)
