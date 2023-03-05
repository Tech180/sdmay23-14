import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

bustype = 'socketcan'
channel = 'vcan0'


lastMonotonicCounter = [0, 0, 0, 0, 0] #to compare to last to ensure only one value changes by +1
currentMonotonicCounter = [0, 0, 0, 0, 0] #each value holds 1 byte or up to 255
t=0 #temp value each time to be stored / updating the montonic value's current byte
#1,099,511,600,000
#setting to CAN FD
bus = can.interfaces.socketcan.SocketcanBus(channel=channel, fd=True) #setting the bus interface to accept CanFD frames
f = open("00x2.txt")
lineCount = 1 #inFuture: convert to bytes to use as freshness value
data_msg=[] # a list of values that will act as the can fd frame as it gets packed into an actual CanFD frame later using a function call in the can library
Sx = bytes.fromhex("00000000111111112222222233333333") #key
#reads 5 lines from the file, adding each to data_msg[], then creates msg to send on bus
for x in f:
    if(lineCount % 5 == 1): #happens once every 5 iterations, this is where cmac and monotonic need to go
        c = cmac.CMAC(algorithms.AES(Sx)) #initialize cmac
        if(t == 255):
            t = 1
        else:
            t+=1
        #storing last monotonic counter value for last fd message sent
        lastMonotonicCounter = currentMonotonicCounter
        #setting monotonic counter value for new canfd message

        if (currentMonotonicCounter[4] != 255): #if bits 1-8 all != 1
            currentMonotonicCounter[4] = t
        elif (currentMonotonicCounter[3] != 255): #if bits 9-16 all != 1
            currentMonotonicCounter[3] = t
        elif (currentMonotonicCounter[2] != 255): #if bits 17-24 all != 1
            currentMonotonicCounter[2] = t
        elif (currentMonotonicCounter[1] != 255): #if bits 25-32 all != 1
            currentMonotonicCounter[1] = t
        elif (currentMonotonicCounter[0] != 255): #if bits 33-40 all != 1
            currentMonotonicCounter[0] = t
        else: #but what if they do?
            #code for new key later down the road, won't reach with current file
            t=0 #rollover
        
    pgn_1 = x[16:18]
    pgn_2 = x[18:20]
    source_address = x[20:22]
    test = ""
    test += str(pgn_1)     
    test += str(pgn_2)
    test += str(source_address)
    
    data_msg.append(int(pgn_1, 16))
    data_msg.append(int(pgn_2, 16))
    data_msg.append(int(source_address, 16))

    for i in range(0,15,2):
        data_msg.append(int(x[i:i+2], 16)) # 8 bytes of data
        test += x[i:i+2]
    testToBytes = bytes(test, 'utf-8')
    c.update(testToBytes)
    if lineCount % 5 == 0:
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
        print("real: ")
        print(msg)

        data_msg=[]
        
    lineCount+=1
    
    #for i in range(len(data_msg)):
     #   print(hex(data_msg[i]))
