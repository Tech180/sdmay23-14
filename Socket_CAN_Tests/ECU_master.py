import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message

from lookupRoutine import get_channel

import signal
import asyncio
from typing import List

import argparse

#Set variables equal to virtual busses running on system
bustype = 'socketcan'
channel_0 = 'vcan0'
channel_2 = 'vcan2'
#Create variables for socketCAN bus channels
vcan0 = can.interfaces.socketcan.SocketcanBus(channel=channel_0)
vcan2 = can.interfaces.socketcan.SocketcanBus(channel=channel_2)

SET_ADDRESS=""

#Sniffs PGN values equal to 8C or broadcast PGN values equal to 240 or greater
def sniffPGN_Broadcast(msg):
    global SET_ADDRESS
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]

    if((pgn_1 == SET_ADDRESS and int(pgn_1,16) < 240) or int(pgn_1,16) >= 240):  #Sniffing the values to print
        print(msg)

def sniffPGN_Direct(msg):
    global SET_ADDRESS
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]

    if(pgn_1 == SET_ADDRESS and int(pgn_1,16) < 240):  #Sniffing the values to print
        print(msg)

def sniff(msg: can.Message) -> None:
    sniffPGN_Direct(msg)
    sniffPGN_Broadcast(msg)

async def main(argv) -> None:
    global SET_ADDRESS
    SET_ADDRESS = argv

    reader = can.AsyncBufferedReader()

    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
        sniff,
    ]

    loop = asyncio.get_running_loop()
    if get_channel(SET_ADDRESS) == "vcan0":
        notifier = can.Notifier(vcan0, listeners, loop=loop) 
    else:
        notifier = can.Notifier(vcan2, listeners, loop=loop) 
        
    while True:
        msg = await reader.get_message()
        #sniffPGN_Broadcast(msg)
        #sniffPGN_Direct(msg)

    notifier.stop()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process address')
    parser.add_argument('--argument', metavar='N', type=str)
    argv = parser.parse_args().argument

    asyncio.run(main(argv))
