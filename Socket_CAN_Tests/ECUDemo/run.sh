#!/bin/bash

x-terminal-emulator -e "python3 getFramesInf.py"
x-terminal-emulator -e "python3 packFrames.py"
x-terminal-emulator -e "python3 receiveFrames.py"
x-terminal-emulator -e "python3 exampleECU.py"