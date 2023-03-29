import time
import can
import math
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message
#from can.listener import MessageRecipient

import signal
import asyncio
from typing import List


#Set variables equal to virtual busses running on system
bustype = 'socketcan'
channel_0 = 'vcan0'
channel_1 = 'vcan1'
channel_2 = 'vcan2'

def handler(signum, frame):
    global dolog, f
    if dolog:
        f.close()
    exit(1)
signal.signal(signal.SIGINT, handler) 

# convert to speed and include backwards compatibility with can and canfd
def speed(mph, extended):
    #1/256 mps
    mps = mph / 2.23694 #convert mph to meter/sec
    
    # 64 bytes long
    if extended:
        # 1/2 ^ 16 calcutates in milliseconds
        # smallest possible increment that can be represented in a CAN FD frame
        byte2 = math.floor(mps/0.00390625) #convert m/s to bytes
        byte1 = math.floor((mps-byte2*0.00390625)/0.00006103516)
    # 8 bytes long
    else:
        # 1/1000
        #  smallest possible increment that can be represented in a CAN frame
        byte2 = math.floor(mps/0.256) #convert m/s to bytes
        byte1 = math.floor((mps-byte2*0.256)/0.001)

    return byte1, byte2

#convert hex message to mph
def pgn(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()
    
    pgn_1 = int (arbitration_ID[0:2], 16) #convert to int
    pgn_2 = int (arbitration_ID[2:4], 16) #convert to int
    
    mps = pgn_2 * 0.256 + pgn_1 * 0.001
    mph = mps * 2.23694

    return pgn_1, pgn_2, mph

#Create variables for socketCAN bus channels
vcan0 = can.interfaces.socketcan.SocketcanBus(channel=channel_0)
vcan1 = can.interfaces.socketcan.SocketcanBus(channel=channel_1)
vcan2 = can.interfaces.socketcan.SocketcanBus(channel=channel_2)

def sniffPGN(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]
    pgn_2 = arbitration_ID[2:4]

    if(pgn_2 == "00" or pgn_2 == "F0" or pgn_2 == "1C" or pgn_2 == "05" or pgn_2 == "1E" or 
       pgn_2 == "8C" or pgn_2 == "13" or pgn_2 == "22" or pgn_2 == "C5" or pgn_2 == "47" or 
       int(pgn_1,16) >= 240):  #Sniffing the values to print
        print(msg)


async def bridge(bus1, bus2):
    while True:
        msg = await bus1.recv()
        await bus2.send(msg)

async def main() -> None:
    #reader = can.AsyncBufferedReader()
    #reader2 = can.AsyncBufferedReader()

    #Async 
    #listeners: List[MessageRecipient] = [
    #    reader,         # AsyncBufferedReader() listener
    #    reader2,        # AsyncBufferedReader() listener for bridge 2
    #]

    loop = asyncio.get_running_loop()

    listener1 = can.Listener()
    listener2 = can.Listener()

    #notifier1 = can.Notifier(vcan0, listeners, loop=loop) 
    #notifier2 = can.Notifier(vcan1, listeners, loop=loop)
    #notifier2 = can.Notifier(vcan2, listeners, loop=loop)
    
    # send outgoing messages
    notifier1 = can.Notifier(vcan0, [listener1, listener2], loop=loop)
    notifier2 = can.Notifier(vcan1, [listener1, listener2], loop=loop)

    # forward messages between buses
    bridge1 = asyncio.create_task(bridge(vcan0, vcan2))
    bridge2 = asyncio.create_task(bridge(vcan1, vcan2))

    # wait until interrupted
    try:
        while True:
            msg = await listener1.get_message()
            sniffPGN(msg)

            msg2 = await listener2.get_message()
            sniffPGN(msg2)
    except KeyboardInterrupt:
        pass

    #while True:
    #    msg = await reader.get_message()
    #    sniffPGN(msg)

    #    msg2 = await reader2.get_message()
    #    sniffPGN(msg2)

if __name__ == "__main__":
    asyncio.run(main())