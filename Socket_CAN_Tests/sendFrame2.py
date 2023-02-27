
import time
import can

bustype = 'socketcan'
channel = 'vcan0'

def run():
    bus = can.interfaces.socketcan.SocketcanBus(channel=channel, fd=True)
    f = open("00x2.txt")
    lineCount = 1;
    data_msg=[]

#reads 5 lines from the file, adding each to data_msg[], then creates msg to send on bus
    for x in f:
        if lineCount % 5 == 0:
            can_id = int(x[16:18] + "" + x[18:20] + x[20:22],16) #PGN & SA
            data_msg.append(can_id)
            data_msg.append(bytes.fromhex(x[0:16]))
            msg = can.Message(arbitration_id=can_id, data=data_msg, is_extended_id=False)
            bus.send(msg)
            data_msg=[]
        else:
            can_id = int(x[16:18] + "" + x[18:20] + x[20:22],16) #PGN & SA
            data_msg.append(can_id)
            data_msg.append(bytes.fromhex(x[0:16]))
        lineCount++

run()
