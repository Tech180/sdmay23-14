import time
import can
import math
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
#from can.message import Message
#from can.listener import MessageRecipient

#from lookupRoutine import get_channel

import signal
import asyncio
from typing import List
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#--------------------------------------------------------Vars for freshness values
last_64_freshness_values=[]
idx_of_next_fv = 0
largest_fv_seen = 0
#---------------------------------------------------------------------------------

#--------------M--------------------------------------------Monotonic counter values
currentMonotonicCounter0 = [0, 0, 0, 0, 0] #for vcan0
t0=1 #temp counter value for vcan0
currentMonotonicCounter1 = [0, 0, 0, 0, 0] #for vcan1
t1=1 #temp counter value for vcan1
#-----------------------------------------------------------------------------------

#-------------CAN DATA FRAMES
data_msg2=[] #to be sent to vcan0
data_msg1=[] #to be sent to vcan1
#----------------------------

#----------------------------------------------------------Cryptography vars
Sx = bytes.fromhex("00000000111111112222222233333333") #key
c = cmac.CMAC(algorithms.AES(Sx))
#---------------------------------------------------------------------------

#------------------------------------------------------------CAN BUS Vars
bustype = 'socketcan'
bus2 = ''              # bus2 connection (for port0)
bus1 = ''              # bus1 connection (for port1)
# globals set by command line arguments (w/ default, if any)
port2 = 'vcan2'
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
""".format(port2, port1)
#----------------------------------------------------------------------------

#------------------------------------------------Everything below this line is for receiving on vcan0 and sending to vcan1
def is_frame_full():
   global data_msg1
   if(len(data_msg1) == 55):
      return True
# signal handler
def handler(signum, frame):
  global dolog, f
  if dolog:
    f.close()
  exit(1)
signal.signal(signal.SIGINT, handler)

def print_message(msg: can.Message) -> None:
    print(msg)

def on_get_message(msg):
  global data_msg1, c
  arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()
  for i in range(0,6-len(arbitration_ID)):
    arbitration_ID = '0' + arbitration_ID
  pgn_1 = arbitration_ID[0:2]
  pgn_2 = arbitration_ID[2:4]
  source_address = arbitration_ID[4:]
  test = ""
  test += str(pgn_1)
  test += str(pgn_2)
  test += str(source_address)
  data_msg1.append(int(pgn_1, 16)) #pgn added to can frame
  data_msg1.append(int(pgn_2, 16)) #pgn added to can frame
  data_msg1.append(int(source_address, 16)) #source address added to can frame
  madeReadable="".join(format(x, '02x') for x in msg.data).upper()
  test += madeReadable  
  for i in range(0,15,2):
    data_msg1.append(int(madeReadable[i:i+2],16)) # 8 bytes of data to be added to the list   
  testToBytes = bytes(test, 'utf-8')
  c.update(testToBytes)

def finalize_send_message_vcan1():
  #Global variables used:
  global data_msg1, t1, currentMonotonicCounter1, c
  #Local operations + vars below
  counterInHex = hex(t1).replace('0x', '')     
  for i in range(0,10-len(counterInHex)):
    counterInHex = '0' + counterInHex
  currentMonotonicCounter1[0]=counterInHex[0:2]
  currentMonotonicCounter1[1]=counterInHex[2:4]
  currentMonotonicCounter1[2]=counterInHex[4:6]
  currentMonotonicCounter1[3]=counterInHex[6:8]
  currentMonotonicCounter1[4]=counterInHex[8:10]
  counterInBytes = bytes(counterInHex, 'utf-8')
  c.update(counterInBytes)
  tag = c.finalize()
  cmactag = (tag.hex())
  first4Bytes = cmactag[:-24] #grabs first 4 bytes of the cmac tag
  hexArray = [int(first4Bytes[0:2], 16), int(first4Bytes[2:4], 16), int(first4Bytes[4:6], 16), int(first4Bytes[6:8], 16)]
  data_msg1.append(hexArray[0]) # 4 bytes of cmac being added to canfd frame
  data_msg1.append(hexArray[1]) # 4 bytes of cmac being added to canfd frame
  data_msg1.append(hexArray[2]) # 4 bytes of cmac being added to canfd frame
  data_msg1.append(hexArray[3]) # 4 bytes of cmac being added to canfd frame
  data_msg1.append(int(str(currentMonotonicCounter1[0]), 16)) # 5 bytes of freshness value being added to canfd frame
  data_msg1.append(int(str(currentMonotonicCounter1[1]), 16)) # 5 bytes of freshness value being added to canfd frame
  data_msg1.append(int(str(currentMonotonicCounter1[2]), 16)) # 5 bytes of freshness value being added to canfd frame
  data_msg1.append(int(str(currentMonotonicCounter1[3]), 16)) # 5 bytes of freshness value being added to canfd frame
  data_msg1.append(int(str(currentMonotonicCounter1[4]), 16)) # 5 bytes of freshness value being added to canfd frame
  msg = can.Message(arbitration_id=0xabc123, data=data_msg1, is_extended_id=True, is_fd=True) #function call involving can library to format it properly into a sendable canfd message for vcan0
  print(msg)
  bus1.send(msg)
  c = cmac.CMAC(algorithms.AES(Sx))
  data_msg1=[]
  t1+=1             
#---------------------------------------------------------------------------------------------------------------------------
def fwd_2to1(msg: can.Message) -> None: # pushes message to vcan0 will be a regular CAN message
    global bus1
    print_message(msg)
    on_get_message(msg)
    if is_frame_full():
      finalize_send_message_vcan1()
#--------------------------------------------------------------------------------------------------- Everything below this line is for receiving on vcan1 and pushing to vcan0
def deconstruct_messages(msg):
  if cmac_validate(msg) and validate_counter(msg):
    print(color.GREEN, "Message Accepted: ", color.END, msg)
    unpack_FD_frame(msg)
        
  elif cmac_validate(msg) and not validate_counter(msg):
    print(color.YELLOW, "Message Fails Counter check: ", color.END, msg)

  elif not cmac_validate(msg) and validate_counter(msg):
    print(color.BLUE, "Message Fails CMAC check: ", color.END, msg)
  else: 
    print(color.RED, "Message Fails Both Counter and CMAC: ", color.END, msg)

def cmac_validate(msg):
    #indexs [..., 55, 56, 57, 58, 59, 60, 61, 62, 63]  - cmac is held in 55-58 (4 bytes)
    cmac_from_received_msg = msg.data[55:59] #gets cmac tag (is in byte array form)
    received_cmac_hex = ''.join(format(x, '02x') for x in cmac_from_received_msg) #converts byte array to hex string

    Sx = bytes.fromhex("00000000111111112222222233333333") #key
    c = cmac.CMAC(algorithms.AES(Sx)) #initialize cmac

    for i in range(0,55,11):
        data_to_cmac="".join(format(x, '02x') for x in msg.data[i:i+11]).upper() # 0-11, 11-22, 22-33, 33-44, 44-55
        data_to_cmac_bytes = bytes(data_to_cmac, 'utf-8')
        c.update(data_to_cmac_bytes)
    data_to_cmac="".join(format(x, '02x') for x in msg.data[59:]) #adding in the counter to cmac update

    data_to_cmac_bytes= bytes(data_to_cmac, 'utf-8')
    c.update(data_to_cmac_bytes)
    expected_cmac_hex = c.finalize().hex()[:-24] 
    
    #print("expcted cmac: ", expected_cmac_hex)
    #print("received cmac: ", received_cmac_hex)
    return expected_cmac_hex == received_cmac_hex

def update_fv_list(fv):
    global last_64_freshness_values
    global idx_of_next_fv
    if len(last_64_freshness_values) == 63:
        last_64_freshness_values.append(int(fv, 16))
        idx_of_next_fv = 0
    elif len(last_64_freshness_values) < 63: 
        last_64_freshness_values.append(int(fv, 16))
        idx_of_next_fv+=1
    else: #list contains 64 elements (start overriding oldest ones)
        last_64_freshness_values[idx_of_next_fv]=fv
        if idx_of_next_fv == 63:
            idx_of_next_fv=0
        else:
            idx_of_next_fv+=1

def smallest_in_FV_list():
    global last_64_freshness_values
    temp = last_64_freshness_values
    temp.sort()
    return temp[0]

def validate_counter(msg):
    global largest_fv_seen
    global last_64_freshness_values
    global idx_of_next_fv

    received_fv="".join(format(x, '02x') for x in msg.data[59:])
    if int(received_fv, 16) > largest_fv_seen:
        largest_fv_seen = int(received_fv, 16)
        update_fv_list(received_fv)
        return True
    if int(received_fv, 16) in last_64_freshness_values:
        return False
    if int(received_fv, 16) < smallest_in_FV_list():
       return False
    update_fv_list(received_fv)
    return True

def unpack_FD_frame(msg):
    global data_msg2 

    for i in range(0,55, 11):
        data_msg2="".join(format(x, '02x') for x in msg.data[i:i+11]).upper() # 0-11, 11-22, 22-33, 33-44, 44-55
        arbitration_ID = data_msg2[0:6]
        data_msg2=data_msg2[6:]
        data_msg0=[int(data_msg2[0:2], 16), int(data_msg2[2:4], 16), int(data_msg2[4:6], 16), int(data_msg2[6:8], 16), int(data_msg2[8:10], 16), int(data_msg2[10:12], 16), int(data_msg2[12:14], 16), int(data_msg2[14:], 16)]
        
        msg0 = can.Message(arbitration_id=int(arbitration_ID,16), data=data_msg0, is_extended_id=True)
        bus2.send(msg0)

def fwd_1to2(msg: can.Message) -> None: # pushes message to vcan1 will be an FD message
    global bus2
    deconstruct_messages(msg)

async def main() -> None:
    """The main function that runs in the loop."""
    global bus2, bus1

    bus2 = can.Bus(interface="socketcan", channel=port2) 
    bus1 = can.Bus(interface="socketcan", channel=port1, fd=True)

    # port1 listeners ..............................................
    reader1 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners1: List[MessageRecipient] = [
        reader1,        # AsyncBufferedReader() listener
        fwd_1to2,       # Callback function
    ]

    # port0 listeners ..............................................
    reader2 = can.AsyncBufferedReader()

    # Listeners are explained in [rtd]/listeners.html
    listeners2: List[MessageRecipient] = [
        reader2,        # AsyncBufferedReader() listener
        fwd_2to1,       # Callback function
    ]
    
    # Create Notifier with an explicit loop to use for scheduling of callbacks
    #   notifier is used as a message distributor for a bus. Notifier
    #   creates a thread to read messages from the bus and distributes
    #   them to listeners. [rtd]/api.html#notifier
    loop1 = asyncio.get_running_loop()
    notifier1 = can.Notifier(bus1, listeners1, loop=loop1)
    loop2 = asyncio.get_running_loop()
    notifier2 = can.Notifier(bus2, listeners2, loop=loop2)

    print("forwarding between %s and %s" %(port2, port1))
    print(" ")
    print("use 'cansniffer' on either or both vcan networks to watch traffic")
    print("..........")
    print("^c to quit")
    while True:
        # Wait for next message from AsyncBufferedReader
        msg1 = await reader1.get_message()
        msg2 = await reader2.get_message()
    # Clean-up
    notifier2.stop()
    notifier1.stop()

if __name__ == "__main__":
    #set_globals(sys.argv[1:])
    asyncio.run(main())