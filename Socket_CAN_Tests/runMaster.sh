#!/bin/bash

x-terminal-emulator -e "python Bidirectional.py"
x-terminal-emulator -e "python Bidirectional2.py"

x-terminal-emulator -e "python ECU_master.py --argument 13"
x-terminal-emulator -e "python ECU_master.py --argument 22"
x-terminal-emulator -e "python ECU_master.py --argument 47"
x-terminal-emulator -e "python ECU_master.py --argument 8C"
x-terminal-emulator -e "python ECU_master.py --argument C5"

x-terminal-emulator -e "python ECU_master.py --argument 00"
x-terminal-emulator -e "python ECU_master.py --argument 05"
x-terminal-emulator -e "python ECU_master.py --argument 1C"
x-terminal-emulator -e "python ECU_master.py --argument 1E"
x-terminal-emulator -e "python ECU_master.py --argument F0"

x-terminal-emulator -e "python getFrames.py"
x-terminal-emulator -e "python getFrames2.py"

