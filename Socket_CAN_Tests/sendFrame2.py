
import time
import can

bustype = 'socketcan'
channel = 'vcan0'

def run():
    #setting to CAN FD
    bus = can.interfaces.socketcan.SocketcanBus(channel=channel, fd=True)
    f = open("00x2.txt")
    lineCount = 1 #inFuture: convert to bytes to use as freshness value
    data_msg=[]

#reads 5 lines from the file, adding each to data_msg[], then creates msg to send on bus
    for x in f:
        print("start of cycle ", lineCount)
        pgn_1 = int(x[16:18], 16)
        pgn_2 = int(x[18:20], 16)
        source_address = int(x[20:22],16)

        data_msg.append(pgn_1)
        data_msg.append(pgn_2)
        data_msg.append(source_address)
        if lineCount % 5 == 0:
            print("flag 1")
        for i in range(0,15,2):
            data_msg.append(int(x[i:i+1], 16))
        if lineCount % 5 == 0:
            print("flag 2")
        if lineCount % 5 == 0:
            msg = can.Message(arbitration_id=0xabc123, data=data_msg, is_extended_id=False)
            bus.send(msg)
            data_msg=[]
            
        lineCount+=1
        print(data_msg)

run()
