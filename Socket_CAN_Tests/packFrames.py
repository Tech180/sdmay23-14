import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message

import signal
import asyncio
from typing import List

bustype = 'socketcan'
channel_0 = 'vcan0'
channel_1 = 'vcan1'

currentMonotonicCounter = [0, 0, 0, 0, 0] #each value holds 1 byte or up to 255
t=1 #temp value each time to be stored / updating the montonic value's current byte
#1,099,511,600,000
#setting to CAN FD
bus = can.interfaces.socketcan.SocketcanBus(channel=channel_1, fd=True) #setting bus to accept CanFD
timeBus = can.interfaces.socketcan.SocketcanBus(channel=channel_0) #setting bus to accept CanFD
lineCount = 1 #inFuture: convert to bytes to use as freshness value
data_msg=[]
Sx = bytes.fromhex("00000000111111112222222233333333") #key

def handler(signum, frame):
  exit(1)
signal.signal(signal.SIGINT, handler)

#reads 5 lines from the file, adding each to data_msg[], then creates msg to send on bus
#TODO / Ideas:
# have a way that a high priority message or X many milliseconds pass, then just send the FD frame
#two ways to do time: 1) using timestamps from file, 2) using can-utils that uses time stamps from file for us
#   could have reading on vcan0 while writing on vcan1 
async def main() -> None:

    reader = can.AsyncBufferedReader()
    listeners: List[MessageRecipient] = [
        reader,         # AsyncBufferedReader() listener
        fwd_1to0,       # Callback function
    ]
    
    loop = asyncio.get_running_loop()
    notifier = can.Notifier(timeBus, listeners, loop=loop) 

    while True:
        msg = await reader.get_message()

        if(lineCount % 5 == 1): #happens once every 5 iterations, this is where cmac and monotonic need to go
            c = cmac.CMAC(algorithms.AES(Sx)) #initialize cmac
        
        print(msg)
        break

        # 3 metadata bytes
        pgn_1 = x[16:18]
        pgn_2 = x[18:20]
        source_address = x[20:22]

        #string we are using for cmac stuff
        test = ""
        test += str(pgn_1)
        test += str(pgn_2)
        test += str(source_address)
        
        #appending to list the meta data bytes
        data_msg.append(int(pgn_1, 16))
        data_msg.append(int(pgn_2, 16))
        data_msg.append(int(source_address, 16))

        for i in range(0,15,2):
            data_msg.append(int(x[i:i+2], 16)) # 8 bytes of data to be added to the list
            test += x[i:i+2]
            
        testToBytes = bytes(test, 'utf-8')
        c.update(testToBytes)

        #Packing frames into FD frames
        if lineCount % 5 == 0: 
            counterInHex = hex(t).replace('0x', '')     
            for i in range(0,10-len(counterInHex)):
                counterInHex = '0' + counterInHex
            currentMonotonicCounter[0]=counterInHex[0:2]
            currentMonotonicCounter[1]=counterInHex[2:4]
            currentMonotonicCounter[2]=counterInHex[4:6]
            currentMonotonicCounter[3]=counterInHex[6:8]
            currentMonotonicCounter[4]=counterInHex[8:10]
            counterInBytes = bytes(counterInHex, 'utf-8')
            c.update(counterInBytes)
            tag = c.finalize()
            cmactag = (tag.hex())
            first4Bytes = cmactag[:-24] #grabs first 4 bytes of the cmac tag
            hexArray = [int(first4Bytes[0:2], 16), int(first4Bytes[2:4], 16), int(first4Bytes[4:6], 16), int(first4Bytes[6:8], 16)]
            data_msg.append(hexArray[0]) # 4 bytes of cmac being added to canfd frame
            data_msg.append(hexArray[1]) # 4 bytes of cmac being added to canfd frame
            data_msg.append(hexArray[2]) # 4 bytes of cmac being added to canfd frame
            data_msg.append(hexArray[3]) # 4 bytes of cmac being added to canfd frame
            data_msg.append(int(str(currentMonotonicCounter[0]), 16)) # 5 bytes of freshness value being added to canfd frame
            data_msg.append(int(str(currentMonotonicCounter[1]), 16)) # 5 bytes of freshness value being added to canfd frame
            data_msg.append(int(str(currentMonotonicCounter[2]), 16)) # 5 bytes of freshness value being added to canfd frame
            data_msg.append(int(str(currentMonotonicCounter[3]), 16)) # 5 bytes of freshness value being added to canfd frame
            data_msg.append(int(str(currentMonotonicCounter[4]), 16)) # 5 bytes of freshness value being added to canfd frame
            msg = can.Message(arbitration_id=0xabc123, data=data_msg, is_extended_id=True, is_fd=True) #function call involving can library to format it properly into a sendable canfd message for vcan0
            bus.send(msg) # this is where the magic happens
            #print("can_data" + "pgn_1: " + pgn_1 + "pgn_2 " + pgn_2 + "source_address "+source_address+ )
            #print("theory: " + test + first4Bytes + currentMonotonicCounter)
            #print("real: ")
            #print(msg)
            #print(lineCount)
            data_msg=[]
            t+=1
            
        lineCount+=1
        #for i in range(len(data_msg)):
        #   print(hex(data_msg[i]))

if __name__ == "__main__":
    asyncio.run(main())