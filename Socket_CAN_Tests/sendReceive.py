import asyncio
from typing import List

import can
#from can.notifier import MessageRecipient
from can.message import Message

# use this to catch ^c (the SIGINT signal) and exit out 
# of infinite loop more gracefully
import signal

# signal handler
def handler(signum, frame):
  exit(1)
signal.signal(signal.SIGINT, handler)

bus0 = can.interfaces.socketcan.SocketcanBus(channel="vcan0", fd=True)
bus1 = can.interfaces.socketcan.SocketcanBus(channel="vcan1", fd=True)

def print_message(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    print(msg)

def fwd_1to0(msg: can.Message) -> None:
    """Regular callback function. Can also be a coroutine."""
    bus0.send(msg)
    #bus1.send(msg)


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

    notifier = can.Notifier(bus0, listeners, loop=loop) 
    #notifier = can.Notifier(bus1, listeners, loop=loop) 


    # Start sending first message
    ##bus.send(can.Message(arbitration_id=0))

    print("forwarding from vcan1 to vcan0 -- use 'cansniffer' to watch traffic")
    print("                               -- ^c to quit")
    while True:
        # Wait for next message from AsyncBufferedReader
        msg = await reader.get_message()
        
        #TODO, scehovic and i were thinking about here's where the msg rejection code goes
        # so to get an idea for how this would work is we are getting the msg right?
        # lets try and reverse engineer it, see if you can put certain things into a list
        # and then start making them their own variables, like can message 1, 2, 3....
        # and so on like we did with the original thing john gave us that we extracted in c
        # with the stuff broken down then, we can copy the same key from testinghex.py into
        # this file and run the cmac algorithm on it all again (or look up if there is a verify
        # function and go from there. like maybe an if != correct verification print out a msg
        # that says "BAD MESSAGE", and a way to actually test this would be maybe find a 
        # function like how we have sleep in C, see if something like that is in python
        # and go implement that in testinghex.py like a message each second or two (there is
        # like 500 or so of them (3550 / 5))













        print(msg)
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
