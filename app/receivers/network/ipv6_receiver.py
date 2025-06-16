import struct

from app.utils import formatter
from ..network_receiver import NetworkReceiver

class IPv6Receiver(NetworkReceiver):
    next_protocol: int

    def __init__(self):
        self.protocol_name = "IPv6"
        self.header_index  = 14
        self.header_size   = 40

    def receive(self, timestamp, data) -> str:
        """Process the received data and return a string list, ready to be written to CSV."""
        header              = struct.unpack('!IHBB16s16s', data[:self.header_size])
        total_len           = header[2]
        self.next_protocol  = header[3]
        src_ip              = formatter.ipv6_format(header[5])
        dst_ip              = formatter.ipv6_format(header[6])

        if ((dst_ip == '::1') or (src_ip == '::1')): # Skip WSL shenanigans
            return None
        return self.assemble_return(timestamp, src_ip, dst_ip, self.next_protocol, total_len)

    def get_protocol_data(self) -> int:
        """Return the Transport protocol number."""
        return self.next_protocol
