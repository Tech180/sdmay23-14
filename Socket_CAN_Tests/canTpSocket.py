from socketcan import *


interface = "vcan0"
rx_addr = 0x7e0
tx_addr = 0x7e8
s = CanIsoTpSocket(interface=interface, rx_addr=rx_addr, tx_addr=tx_addr)
data = bytes(list(range(64)))
s.send(data)
