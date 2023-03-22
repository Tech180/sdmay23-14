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

def sniffPGN(msg):
    #print(hex(msg.arbitration_id))
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()
    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID
    pgn_1 = arbitration_ID[0:2]
    pgn_2 = arbitration_ID[2:4]
    source_address = arbitration_ID[4:]
    if(pgn_1+pgn_2 == "1CFE"):
        print(msg)

async def main() -> None:
    reader = can.AsyncBufferedReader()

    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
    ]

    loop = asyncio.get_running_loop()
    notifier = can.Notifier(vcan2, listeners, loop=loop) 

    while True:
        msg = await reader.get_message()
        sniffPGN(msg)

        #vcan1.send(msg)

if __name__ == "__main__":
    asyncio.run(main())