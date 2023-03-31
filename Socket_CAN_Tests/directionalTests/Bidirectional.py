import time
import can
import math
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message

import signal
import asyncio
from typing import List

#Set variables equal to virtual busses running on system
bustype = 'socketcan'
channel_0 = 'vcan0'
channel_1 = 'vcan1'
channel_2 = 'vcan2'

#Create variables for socketCAN bus channels
vcan0 = can.interfaces.socketcan.SocketcanBus(channel=channel_0)
vcan1 = can.interfaces.socketcan.SocketcanBus(channel=channel_1)
vcan2 = can.interfaces.socketcan.SocketcanBus(channel=channel_2)

def handler(signum, frame):
    global dolog, f
    if dolog:
        f.close()
    exit(1)
signal.signal(signal.SIGINT, handler) 

#get speed values
def speed(mph):
    mps = mph / 2.23694 #convert mph to meter/sec
    byte2 = math.floor(mps/0.256) #convert m/s to bytes
    byte1 = math.floor((mps-byte2*0.256)/0.001)
    return byte1, byte2

#convert hex message to mph
def pgn(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()
    pgn_1 = arbitration_ID[0:2]
    pgn_2 = arbitration_ID[2:4]
    mps = pgn_2 * 0.256 + pgn_1 * 0.001
    mph = mps * 2.23694
    return pgn_1, pgn_2, mph

def default_0(msg: can.Message) -> None:
        global channel_0
        msg = sniffPGN(msg)
        pgn(msg)
        speed(msg)
        channel_0.send(msg)

def fwd_0to1(msg: can.Message) -> None:
        global channel_0
        msg = sniffPGN(msg)
        pgn(msg)
        speed(msg)
        channel_1.send(msg)

def fwd_1to2(msg: can.Message) -> None:
        global channel_1
        msg = sniffPGN(msg)
        pgn(msg)
        speed(msg)
        channel_2.send(msg)

def fwd_2to1(msg: can.Message) -> None:
        global channel_2
        msg = sniffPGN(msg)
        pgn(msg)
        speed(msg)
        channel_1.send(msg)

def fwd_1to0(msg: can.Message) -> None:
        global channel_1
        msg = sniffPGN(msg)
        pgn(msg)
        speed(msg)
        channel_0.send(msg)

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

async def main() -> None:
    reader = can.AsyncBufferedReader()

    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
        fwd_0to1,       # Callback function
        fwd_1to2,       # Callback function
        fwd_2to1,       # Callback function
        fwd_1to0        # Callback function
    ]

    loop0 = asyncio.get_running_loop()
    notifier0 = can.Notifier(vcan0, listeners, loop=loop0) 
    loop1 = asyncio.get_running_loop()
    notifier1 = can.Notifier(vcan1, listeners, loop=loop1)
    loop2 = asyncio.get_running_loop()
    notifier2 = can.Notifier(vcan2, listeners, loop=loop2)

    while True:
        msg = await reader.get_message()
        fwd_0to1(msg)
        fwd_1to2(msg)
        fwd_2to1(msg)
        fwd_1to0(msg)
        
if __name__ == "__main__":
    asyncio.run(main())
