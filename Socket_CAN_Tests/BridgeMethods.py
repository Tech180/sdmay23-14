import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message

import signal
import asyncio
from typing import List

from lookupRoutine import get_channel

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

bus_0 = can.interfaces.socketcan.SocketcanBus(channel="vcan0") 
bus_1= can.interfaces.socketcan.SocketcanBus(channel="vcan1", fd=True)
bus_2 = can.interfaces.socketcan.SocketcanBus(channel="vcan2") 

currentMonotonicCounter = [0, 0, 0, 0, 0] 
Sx = bytes.fromhex("00000000111111112222222233333333")
data_msg=[]

def cmac_validate(msg):
    #indexs [..., 55, 56, 57, 58, 59, 60, 61, 62, 63]  - cmac is held in 55-58 (4 bytes)
    cmac_from_received_msg = msg.data[55:59] #gets cmac tag (is in byte array form)
    received_cmac_hex = ''.join(format(x, '02x') for x in cmac_from_received_msg) #converts byte array to hex string

    global Sx
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
    data_msg=[] 

    for i in range(0,55, 11):
        data_msg="".join(format(x, '02x') for x in msg.data[i:i+11]).upper() # 0-11, 11-22, 22-33, 33-44, 44-55
        arbitration_ID = data_msg[0:6]
        data_msg=data_msg[6:]
        data_msg2=[int(data_msg[0:2], 16), int(data_msg[2:4], 16), int(data_msg[4:6], 16), int(data_msg[6:8], 16), int(data_msg[8:10], 16), int(data_msg[10:12], 16), int(data_msg[12:14], 16), int(data_msg[14:], 16)]
        
        msg2 = can.Message(arbitration_id=int(arbitration_ID,16), data=data_msg2, is_extended_id=True)
        bus2.send(msg2)

def try_to_validate(msg):
    if cmac_validate(msg) and validate_counter(msg):
        print(color.GREEN, "Message Accepted: ", color.END, msg)
        unpack_FD_frame(msg)
        
    elif cmac_validate(msg) and not validate_counter(msg):
        print(color.YELLOW, "Message Fails Counter check: ", color.END, msg)

    elif not cmac_validate(msg) and validate_counter(msg):
        print(color.BLUE, "Message Fails CMAC check: ", color.END, msg)
    else: 
        print(color.RED, "Message Fails Both Counter and CMAC: ", color.END, msg)


#this is just for normal CAN frames (NOT can FD)
async def receive_CAN_frame(busToUse):
    countReceived = 0
    if busToUse == "bus_0" or busToUse == "bus_2":
        reader = can.AsyncBufferedReader()

        listeners: List[MessageRecipient] = [
            reader
        ]
        
        loop = asyncio.get_running_loop()
        if busToUse == "bus_0":
            notifier = can.Notifier(bus_0, listeners, loop=loop) 
        else: 
            notifier = can.Notifier(bus_2, listeners, loop=loop) 
        
        while countReceived < 5:
            msg = await reader.get_message()
            countReceived+=1
            pack_frames(msg)

    return 0


def pack_frames():
    arbitration_ID = hex(msg.arbitration_id).replace("0x", "").upper()
    for i in range(0,6-len(arbitration_ID)):
        arbitration_ID = '0' + arbitration_ID
    source_address = arbitration_ID[4:]
    #print(lineCount, source_address, type(source_address), get_channel(source_address))
    if get_channel(source_address) == "vcan2":
        #print("passed")
        #time.sleep(5)
        if(lineCount % 5 == 1): #happens once every 5 iterations, this is where cmac and monotonic need to go
            c = cmac.CMAC(algorithms.AES(Sx)) #initialize cmac
        
        pgn_1 = arbitration_ID[0:2]
        pgn_2 = arbitration_ID[2:4]
        source_address = arbitration_ID[4:]

        #string we are using for cmac stuff
        test = ""
        test += str(pgn_1)
        test += str(pgn_2)
        test += str(source_address)
        
        print(msg)

        global data_msg
        #appending to list the meta data bytes
        data_msg.append(int(pgn_1, 16))
        data_msg.append(int(pgn_2, 16))
        data_msg.append(int(source_address, 16))
        

        madeReadable="".join(format(x, '02x') for x in msg.data).upper()
        for i in range(0,15,2):
            data_msg.append(int(madeReadable[i:i+2],16)) # 8 bytes of data to be added to the list
        test += madeReadable
            
        testToBytes = bytes(test, 'utf-8')
        c.update(testToBytes)

        #Packing frames into FD frames
        if lineCount % 5 == 0: 
            counterInHex = hex(t).replace('0x', '')     
            for i in range(0,10-len(counterInHex)):
                counterInHex = '0' + counterInHex
            global currentMonotonicCounter
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
            print(msg)
            bus_1.send(msg)

            data_msg=[]
            t+=1
            
        lineCount+=1

def listen_for_FD_frame():

    return
