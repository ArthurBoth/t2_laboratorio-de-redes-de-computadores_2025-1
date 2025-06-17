import struct

from app.utils import formatter
from .receiver import Receiver

class EthernetReceiver(Receiver):
    eth_hex: int

    def __init__(self):
        self.protocol_name = "Ethernet"
        self.header_index  = 0
        self.header_size   = 14

    def receive(self, timestamp: str, raw_data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        ethernet_data = struct.unpack('!6s6sH', raw_data[self.header_index:self.header_size])
        dest_mac      = formatter.mac_format(ethernet_data[0])
        src_mac       = formatter.mac_format(ethernet_data[1])
        self.eth_hex  = ethernet_data[2]
        total_len     = len(raw_data)

        if (src_mac == '00:00:00:00:00:00'): # Skip WSL shenanigans
            return None
        return self.assemble_return(timestamp, src_mac, dest_mac, self.eth_hex, total_len)

    def get_protocol_data(self) -> int:
        """Return the Network protocol number."""
        return self.eth_hex
