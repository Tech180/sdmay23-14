import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message

import signal
import asyncio
from typing import List

bustype = 'socketcan'
channel_2 = 'vcan2'

# signal handler
def handler(signum, frame):
  exit(1)
signal.signal(signal.SIGINT, handler)

bus = can.interfaces.socketcan.SocketcanBus(channel=channel_2) #setting bus to accept CanFD from vcan2

def read_message(msg):
    data_msg=[]

    for i in range(0,55, 11):
        msg = can.Message(arbitration_id=int(arbitration_ID,16), data=data_msg, is_extended_id=True)
        bus.send(msg)

#def match_PGN(msg):
    #this function will match PGN values to accept the message

#def broadcast(msg):
    #this function will detect if it is a broadcast message to accept

async def main() -> None:

    reader = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
    ]

    loop = asyncio.get_running_loop()
    notifier = can.Notifier(bus, listeners, loop=loop) 

    while True:
        # Wait for next message from AsyncBufferedReader
        msg = await reader.get_message()
        #if match_PGN and not broadcast(msg)
            #read_message(msg)
        #if not match_PGN and broadcast(msg)
            #read_message(msg)
        #if not match_PGN and broadcast(msg)
            #fails
        read_message(msg) #remove after match_PGN and broadcast are done being implemented, this is here for testing
        

if __name__ == "__main__":
    asyncio.run(main())

    
