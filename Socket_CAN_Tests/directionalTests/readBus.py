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

async def main() -> None:
    reader = can.AsyncBufferedReader()

    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
    ]

    loop = asyncio.get_running_loop()
    notifier = can.Notifier(vcan2, listeners, loop=loop) 

    while True:
        msg = await reader.get_message()
        print(msg)

if __name__ == "__main__":
    asyncio.run(main())