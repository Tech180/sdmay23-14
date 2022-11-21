How to compile & run:
1) type in: make
2) run: ./Main 00x
*note: 00x is the parameter passed in - it can be any ECU type from CAN bus log file


Phase 2 Goals:
- better simulate CAN network
    - breaking apart code from last demo into ECUs (for example braking, engine, transmission) where each one only reads those lines from file
    - adding in bridge aspect (this is where encryption/decryption will happen)

Main.h:
- all the imports

ECU.c: 
- simulates an ECU (makes call to function in Bridge.c for each line where parameter passed in matches line from file)

Bridge.c 
- simulates Bridge (encrypt/decrypt, build CAN fd frames, etc)

