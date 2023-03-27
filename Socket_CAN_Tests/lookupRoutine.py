from . import addressConstants

# Address dictionary. Contains all addressable nodes in the network
sourceAddrTable = {
    "vcan2" : [SOURCE_ADDRESS_0, SOURCE_ADDRESS_1, SOURCE_ADDRESS_2, SOURCE_ADDRESS_3, SOURCE_ADDRESS_4],
    "vcan0" : [SOURCE_ADDRESS_5, SOURCE_ADDRESS_6, SOURCE_ADDRESS_7, SOURCE_ADDRESS_8, SOURCE_ADDRESS_9]
}

isAddrInTable = False

# Iterate through dictionary and test if source_address matches an address in the dictionary
# TODO: Possibly optimize function if too slow for our use-case ( currently running O^2 time :\ ) 
def lookForAddr(source_address):
    for channel in sourceAddrTable:
        for addr in channel:
            if(addr == source_addr):
                isAddrInTable = True
                break
        else: 
            continue
        break
    
    return isAddrInTable


