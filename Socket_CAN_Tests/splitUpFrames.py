

# vcan0
SOURCE_ADDRESS_8C = "8C"
SOURCE_ADDRESS_13 = "13"
SOURCE_ADDRESS_22 = "22"
SOURCE_ADDRESS_C5 = "C5"
SOURCE_ADDRESS_47 = "47"

vcan0 = [SOURCE_ADDRESS_8C, SOURCE_ADDRESS_13, SOURCE_ADDRESS_22, SOURCE_ADDRESS_C5, SOURCE_ADDRESS_47]

# vcan2
SOURCE_ADDRESS_00 = "00"
SOURCE_ADDRESS_F0 = "F0"
SOURCE_ADDRESS_1C = "1C"
SOURCE_ADDRESS_05 = "05"
SOURCE_ADDRESS_1E = "1E"

vcan2 = [SOURCE_ADDRESS_00, SOURCE_ADDRESS_F0, SOURCE_ADDRESS_1C, SOURCE_ADDRESS_05, SOURCE_ADDRESS_1E]

f = open("00x_time.txt")
f_vcan0 = open("vcan0_CAN_frames", "a")
f_vcan2 = open("vcan2_CAN_frames", "a")

for x in f:
    pgn_1 = x[16:18]
    pgn_2 = x[18:20]
    source_address = x[20:22]

    if source_address in vcan0:
        f_vcan0.write(x)
    elif source_address in vcan2:
        f_vcan2.write(x)
    
