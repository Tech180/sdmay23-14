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
channel_0 = 'vcan0'

#Create variables for socketCAN bus channels
vcan0 = can.interfaces.socketcan.SocketcanBus(channel=channel_0)

#Sniffs PGN values equal to 8C or broadcast PGN values equal to 240 or greater
def sniffPGN_Broadcast(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]

    if((pgn_1 == "8C" and int(pgn_1,16) < 240) or int(pgn_1,16) >= 240):  #Sniffing the values to print
        print(msg)

def sniffPGN_Direct(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]

    if(pgn_1 == "8C" and int(pgn_1,16) < 240):  #Sniffing the values to print
        print(msg)

async def main() -> None:
    reader = can.AsyncBufferedReader()

    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
    ]

    loop = asyncio.get_running_loop()
    notifier = can.Notifier(vcan0, listeners, loop=loop) 

    while True:
        msg = await reader.get_message()
        #sniffPGN_Broadcast(msg)
        sniffPGN_Direct(msg)

if __name__ == "__main__":
    asyncio.run(main())