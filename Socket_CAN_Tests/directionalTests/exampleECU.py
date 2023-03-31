import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message

import signal
import asyncio
from typing import List

#Set variables equal to virtual busses running on system
bustype = 'socketcan'
channel_2 = 'vcan2'
channel_1 = 'vcan1'

#Create variables for socketCAN bus channels
vcan1 = can.interfaces.socketcan.SocketcanBus(channel=channel_1)
vcan2 = can.interfaces.socketcan.SocketcanBus(channel=channel_2)

#Sniffs PGN_2 value (destination address) equal to FE or PGN_1 value equal to 240 or greater (broadcast message)
def sniffPGN_Broadcast(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]
    pgn_2 = arbitration_ID[2:4]

    if((pgn_2 == "FE" and int(pgn_1,16) < 240) or int(pgn_1,16) >= 240):  #Sniffing the values to print
        print(msg)

#Only sniffs direct messages (no broadcast messages)
def sniffPGN_direct(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]
    pgn_2 = arbitration_ID[2:4]

    if((pgn_2 == "FE" and int(pgn_1,16) < 240)):  #Sniffing the values to print
        print(msg)

async def main() -> None:
    reader = can.AsyncBufferedReader()
    mode = 1
    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
    ]

    loop = asyncio.get_running_loop()
    notifier = can.Notifier(vcan2, listeners, loop=loop) 

    while True:
        msg = await reader.get_message()
        if(mode == 0):
            sniffPGN_Broadcast(msg)
        else:
            sniffPGN_direct(msg)

if __name__ == "__main__":
    asyncio.run(main())