import time
import can
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import algorithms
from can.message import Message
import signal
import asyncio
from typing import List

from lookupRoutine import get_channel
from BridgeMethods import receive_CAN_frame, pack_frames, listen_for_FD_frame
from BridgeMethods import bus_0, bus_1, bus_2



async def main() -> None:
    
    while True:
        receive_CAN_frame("bus_0")
        listen_for_FD_frame() #always bus_1 so don't need to specify which bus



if __name__ == "__main__":
    asyncio.run(main())