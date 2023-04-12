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
channel_1 = 'vcan1'

#Create variables for socketCAN bus channels
vcan0 = can.interfaces.socketcan.SocketcanBus(channel=channel_0)
vcan1 = can.interfaces.socketcan.SocketcanBus(channel=channel_1)

#Sniffs PGN values equal to 1CFE or broadcast PGN values equal to 240 or greater
def sniffPGN(msg):
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()  #arbitration_ID containing pgn_1 and pgn_2

    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID   #Adding leading zeros to ID

    pgn_1 = arbitration_ID[0:2]
    pgn_2 = arbitration_ID[2:4]

    if(pgn_2 == "22" or int(pgn_1,16) >= 240):  #Sniffing the values to print
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
        sniffPGN(msg)

if __name__ == "__main__":
    asyncio.run(main())