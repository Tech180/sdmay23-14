import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

bustype = 'socketcan'
channel = 'vcan0'

#setting to CAN FD
bus = can.interfaces.socketcan.SocketcanBus(channel=channel, fd=True)
f = open("00x2.txt")
lineCount = 1 #inFuture: convert to bytes to use as freshness value
data_msg=[]
Sx = bytes.fromhex("00000000111111112222222233333333") #key
#reads 5 lines from the file, adding each to data_msg[], then creates msg to send on bus
for x in f:
    if(lineCount % 5 == 1):
        c = cmac.CMAC(algorithms.AES(Sx)) #initialize cmac
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
        data_msg.append(hexArray[0])
        data_msg.append(hexArray[1])
        data_msg.append(hexArray[2])
        data_msg.append(hexArray[3])
        msg = can.Message(arbitration_id=0xabc123, data=data_msg, is_extended_id=True, is_fd=True)
        bus.send(msg) 
        #print("can_data" + "pgn_1: " + pgn_1 + "pgn_2 " + pgn_2 + "source_address "+source_address+ )
        print("theory: " + test + first4Bytes)
        print("real: ")
        print(msg)

        data_msg=[]
        
    lineCount+=1
    
    #for i in range(len(data_msg)):
     #   print(hex(data_msg[i]))
