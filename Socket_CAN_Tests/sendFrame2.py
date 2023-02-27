
import time
import can

bustype = 'socketcan'
channel = 'vcan0'

def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    #bus = can.Bus(channel=channel, interface=bustype)
    bus = can.interfaces.socketcan.SocketcanBus(channel='vcan0', fd=True)
    for i in range(10):
        msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], is_extended_id=False)
        bus.send(msg)

    time.sleep(1)

producer(10)
