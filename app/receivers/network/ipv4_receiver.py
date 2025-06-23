import struct

from app.utils import formatter
from app.utils.constants import IGNORE_LOCALHOST, LOCALHOST
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

        if ((IGNORE_LOCALHOST) and ((dst_ip == LOCALHOST) or (src_ip == LOCALHOST))):
            return None
        return self.assemble_return(timestamp, src_ip, dst_ip, self.next_protocol, len(data))

    def assemble_return(self, timestamp, src, dst, protocol, total_len) -> list[str]:
        """Assemble the return string for CSV writing."""
        return [timestamp, self.protocol_name, src, dst, protocol, total_len]

    def get_protocol_data(self) -> int:
        """Return the Transport protocol number."""
        return self.next_protocol
