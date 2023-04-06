#!/bin/bash

x-terminal-emulator -e "python3 getFrames.py"
x-terminal-emulator -e "python3 packFrames.py | tee outputData/packFrames.txt"
x-terminal-emulator -e "python3 receiveFrames.py | tee outputData/receiveFrames.txt"