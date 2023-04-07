import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms

bustype = 'socketcan'
channel_0 = 'vcan0'

timeBus = can.interfaces.socketcan.SocketcanBus(channel=channel_0) #setting bus 

data_msg=[]

f = open("00x_time.txt")

previous_time = 0

for x in f:
    current_time = float(x[23:].replace("\n",""))

    # 3 metadata bytes
    pgn_1 = x[16:18]
    pgn_2 = x[18:20]
    source_address = x[20:22]

    for i in range(0,15,2):
        data_msg.append(int(x[i:i+2], 16)) # 8 bytes of data to be added to the list

    msg = can.Message(arbitration_id=int(pgn_1+pgn_2+source_address,16), data=data_msg, is_extended_id=True) #function call involving can library to format it properly into a sendable canfd message for vcan0
    
    if previous_time != 0 and current_time - previous_time > 0:
        time.sleep(current_time - previous_time)
        #print(current_time-previous_time) #Print out the time between each message being sent
    print(msg)
    timeBus.send(msg)
    data_msg=[] #data needs to be cleared so you aren't appending multiple messages together
    previous_time = current_time