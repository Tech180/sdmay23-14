How to run the code in Phase4?

1) compile with: make
2) run with: ./Main 00x

What does the output mean?
- there is one line of output for each CAN frame, plus additional output after every 5 lines
that gives information on the CMAC that is made from the previous 5 messages

this additional output can be broken down by:
- CanData = print out of the 5 messages combined 
- CMAC Tag = prints 5 bytes of hex (taken from the 16 byte CMAC we get)
- 2 arrays 'mact' and 'finalCMAC' = print out what is being copied over at each index, this is where we sometimes see only 1 of the 2 hex digits being copied over

- ends with 2 new lines

