
x-terminal-emulator -e "python3 getFramesInf.py"
x-terminal-emulator -e "python3 packFrames.py"
x-terminal-emulator -e "python3 receiveFrames.py"

x-terminal-emulator -e "python3 ECU_master.py 13"
x-terminal-emulator -e "python3 ECU_master.py 22"
x-terminal-emulator -e "python3 ECU_master.py 47"
x-terminal-emulator -e "python3 ECU_master.py 8C"
x-terminal-emulator -e "python3 ECU_master.py C5"

x-terminal-emulator -e "python3 ECU_master.py 00"
x-terminal-emulator -e "python3 ECU_master.py 05"
x-terminal-emulator -e "python3 ECU_master.py 1C"
x-terminal-emulator -e "python3 ECU_master.py 1E"
x-terminal-emulator -e "python3 ECU_master.py F0"
