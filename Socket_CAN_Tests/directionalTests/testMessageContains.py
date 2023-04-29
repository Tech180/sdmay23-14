import time
import can
import math
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
#from can.message import Message
#from can.listener import MessageRecipient



import signal
import asyncio
from typing import List


bustype = 'socketcan'
bus0 = ''              # bus0 connection (for port0)
bus1 = ''              # bus1 connection (for port1)
f = ''                 # file handle for log file

# globals set by command line arguments (w/ default, if any)
port0 = 'vcan0'
port1 = 'vcan1'
filename = 'debug.txt'
verbose = False
dolog = False        # true when we should write to file

usage = """
-0  --port0  <bus_name>    set bus connected to port 0
-1  --port1  <bus_name>    set bus connected to port 1
-o  --out    <file_name>   save a copy of the forwarded data in a log file
-v                         verbose output to show port values being used
if -o / --out is not specified then no file is created.
default: --port0 {0} --port1 {1} 
""".format(port0, port1)

# signal handler
def handler(signum, frame):
  global dolog, f
  if dolog:
    f.close()
  exit(1)
signal.signal(signal.SIGINT, handler)

def print_message(msg: can.Message) -> None:
    print(msg)

def write_message(msg: can.Message) -> None:
    global dolog, f
    if dolog:
      f.write(msg.__str__())
      f.write("\n")

def fwd_0to1(msg: can.Message) -> None: # pushes message to vcan0 will be a regular CAN message
    global bus1
    bus1.send(msg)
    write_message(msg)

def fwd_1to0(msg: can.Message) -> None: # pushes message to vcan1 will be an FD message
    global bus0
    bus0.send(msg)
    write_message(msg)

def set_globals(argv):
  global port0, port1, verbose, filename, dolog
  #try:
  #  opts, args = getopt.getopt(argv, "hv0:1:o:",["port0=","port1=","out="])
  #except getopt.GetoptError as err:
  #  print(err)
  #  print(usage)
  #  sys.exit(2)
  #for opt, arg in opts:
  #  if opt == "-h":
  #   print(usage)
  #    sys.exit()
  #  elif opt == "-v":
  #    verbose = True
  #  elif opt in ("-0", "--port0"):
  #    port0 = arg
  #  elif opt in ("-1", "--port1"):
  #    port1 = arg
  #  elif opt in ("-o", "--out"):
  #   dolog = True
  #   filename = arg

  if verbose:
    print("   port0: %s" % (port0))
    print("   port1: %s" % (port1))
    print("filename: %s" % (filename))
    print(" logging: %s" % (dolog))

async def main() -> None:
    """The main function that runs in the loop."""
    global bus0, bus1, dolog, f
    isVcan2=False
    data_msg=[]
    lineCount = 1 #inFuture: convert to bytes to use as freshness value
    t=1 #temp value each time to be stored / updating the montonic value's current byte
    currentMonotonicCounter = [0, 0, 0, 0, 0] #each value holds 1 byte or up to 255
    Sx = bytes.fromhex("00000000111111112222222233333333") #key

    bus0 = can.Bus(interface="socketcan", channel=port0) 
    bus1 = can.Bus(interface="socketcan", channel=port1, fd=True)

    if dolog:
      f = open(filename, "w")

    # port1 listeners ..............................................
    reader1 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners1: List[MessageRecipient] = [
        reader1,        # AsyncBufferedReader() listener
        fwd_1to0,       # Callback function
    ]

    # port0 listeners ..............................................
    reader0 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners0: List[MessageRecipient] = [
        reader0,        # AsyncBufferedReader() listener
        fwd_0to1,       # Callback function
    ]
    
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    #   notifier is used as a message distributor for a bus. Notifier
    #   creates a thread to read messages from the bus and distributes
    #   them to listeners. [rtd]/api.html#notifier
    loop1 = asyncio.get_running_loop()
    notifier1 = can.Notifier(bus1, listeners1, loop=loop1)
    loop0 = asyncio.get_running_loop()
    notifier0 = can.Notifier(bus0, listeners0, loop=loop0)

    print("forwarding between %s and %s" %(port0, port1))
    print(" ")
    print("use 'cansniffer' on either or both vcan networks to watch traffic")
    print("..........")
    print("^c to quit")
    while True:
        # Wait for next message from AsyncBufferedReader
        msg1 = await reader1.get_message()
        msg0 = await reader0.get_message()
        print("Message 1 contains ", msg1)
        print("Message 0 contains ",msg0)


if __name__ == "__main__":
    asyncio.run(main())