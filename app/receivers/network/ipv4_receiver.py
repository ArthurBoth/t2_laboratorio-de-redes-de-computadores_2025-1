import struct

from app.utils import formatter
from ..receiver import Receiver

class IPv4Receiver(Receiver):
    next_protocol: int

    def __init__(self):
        self.protocol_name = "IPv4"
        self.header_index  = 14
        self.header_size   = 20

    def receive(self, timestamp, data) -> str:
        """Process the received data and return a string list, ready to be written to CSV."""
        header             = struct.unpack('!BBHHHBBH4s4s', data[:self.header_size])
        self.header_size   = header[2]
        self.next_protocol = header[6]
        src_ip             = formatter.ipv4_format(header[8])
        dst_ip             = formatter.ipv4_format(header[9])

        if ((dst_ip == '127.0.0.1') or (src_ip == '127.0.0.1')): # Skip WSL shenanigans
            return None
        return self.assemble_return(timestamp, src_ip, dst_ip, self.next_protocol, len(data))

    def get_protocol_data(self) -> int:
        """Return the Transport protocol number."""
        return self.next_protocol
