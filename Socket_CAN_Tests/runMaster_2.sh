#!/bin/bash

x-terminal-emulator -e "python Bidirectional.py"
x-terminal-emulator -e "python Bidirectional2.py"

x-terminal-emulator -e "python ECU_master.py --argument 8C"
x-terminal-emulator -e "python ECU_master.py --argument 00"

x-terminal-emulator -e "python getFrames.py"
x-terminal-emulator -e "python getFrames2.py"

