import addressConstants
import time 

# Address dictionary. Contains all addressable nodes in the network
source_address_table = {
    "vcan0" : [addressConstants.SOURCE_ADDRESS_8C, addressConstants.SOURCE_ADDRESS_13,
                addressConstants.SOURCE_ADDRESS_22, addressConstants.SOURCE_ADDRESS_C5, 
                addressConstants.SOURCE_ADDRESS_47],
    "vcan2" : [addressConstants.SOURCE_ADDRESS_00, addressConstants.SOURCE_ADDRESS_F0, 
               addressConstants.SOURCE_ADDRESS_1C, addressConstants.SOURCE_ADDRESS_05, 
               addressConstants.SOURCE_ADDRESS_1E]
    
}

# Iterate through dictionary and test if source_address matches an address in the dictionary
# TODO: Possibly optimize function if too slow for our use-case ( currently running O^2 time :\ ) 
def get_channel(source_address):
    for channel in source_address_table:
        for address in source_address_table.get(channel):
            if address == source_address:
                return channel
    return ""


