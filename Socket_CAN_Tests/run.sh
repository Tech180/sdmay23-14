#!/bin/bash

x-terminal-emulator -e "python3 getFrames.py"
x-terminal-emulator -e "python3 packFrames.py 2> /home/user/Desktop/sdmay23-14/Socket_CAN_Tests/outputData/packFrames.txt"
x-terminal-emulator -e "python3 receiveFrames.py 2> /home/user/Desktop/sdmay23-14/Socket_CAN_Tests/outputData/receiveFrames.txt"