#!/bin/bash

x-terminal-emulator -e "python3 packFrames.py"
x-terminal-emulator -e "python3 receiveFrames.py"
x-terminal-emulator -e "python3 getFrames.py"