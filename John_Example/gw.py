#!/usr/bin/python3
# source: https://python-can.readthedocs.io/en/master/asyncio.html
#   hereafter, [rtd] = source url through "master/"

"""
This example demonstrates how to use async IO with python-can.
"""

import asyncio
from typing import List

import can
from can.notifier import MessageRecipient

# use this to catch ^c (the SIGINT signal) and exit out 
# of infinite loop more gracefully
import signal

# signal handler
def handler(signum, frame):
  exit(1)
signal.signal(signal.SIGINT, handler)

bus0 = can.Bus(interface="socketcan", channel="vcan0") 
bus1 = can.Bus(interface="socketcan", channel="vcan1") 

def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(msg)

def fwd_1to0(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    bus0.send(msg)


async def main() -> None:
    """The main function that runs in the loop."""

    reader = can.AsyncBufferedReader()
    logger = can.Logger("logfile.asc")

    # Listeners are explained in [rtd]/listeners.html
    listeners: List[MessageRecipient] = [
        ##print_message,  # Callback function
        reader,         # AsyncBufferedReader() listener
        ##logger,        # Regular Listener object
        fwd_1to0,       # Callback function
    ]
    
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    #   notifier is used as a message distributor for a bus. Notifier
    #   creates a thread to read messages from the bus and distributes
    #   them to listeners. [rtd]/api.html#notifier
    loop = asyncio.get_running_loop()
    notifier = can.Notifier(bus1, listeners, loop=loop)
    # Start sending first message
    ##bus.send(can.Message(arbitration_id=0))

    print("forwarding from vcan1 to vcan0 -- use 'cansniffer' to watch traffic")
    print("                               -- ^c to quit")
    while True:
        # Wait for next message from AsyncBufferedReader
        msg = await reader.get_message()
        # Delay response
        ##await asyncio.sleep(0.5)
        msg.arbitration_id += 1
        ##bus.send(msg)

    # Wait for last message to arrive
    await reader.get_message()
    print("Done!")

    # Clean-up
    notifier.stop()


if __name__ == "__main__":
    asyncio.run(main())
