import struct

from app.utils import formatter
from ..receiver import Receiver

EXTENSION_HEADERS = {
    0:  'Hop-by-Hop Options',
    43: 'Routing',
    44: 'Fragment',
    50: 'Encapsulating Security Payload (ESP)',
    51: 'Authentication Header (AH)',
    60: 'Destination Options',
}

class IPv6Receiver(Receiver):
    next_protocol: int

    def __init__(self):
        self.protocol_name = "IPv6"
        self.header_index  = 14
        self.header_size   = 40

    def receive(self, timestamp, data) -> str:
        """Process the received data and return a string list, ready to be written to CSV."""
        header              = struct.unpack('!IHBB16s16s', data[:self.header_size])
        self.next_protocol  = header[3]
        src_ip              = formatter.ipv6_format(header[5])
        dst_ip              = formatter.ipv6_format(header[6])

        if ((dst_ip == '::1') or (src_ip == '::1')): # Skip WSL shenanigans
            return None
        return self.assemble_return(timestamp, src_ip, dst_ip, self.next_protocol, len(data))

    def get_protocol_data(self) -> int:
        """Return the Transport protocol number."""
        return self.next_protocol

    def check_extension_headers(self, next_header: int, data: bytes) -> int:
        """Check for extension headers, sets the header size and next protocol."""
        offset = self.header_size

        while (next_header in EXTENSION_HEADERS):
            if (len(data) < (offset + 2)):
                break

            next_header_pos         = data[offset    ]
            extension_header_length = data[offset + 1]

            if next_header == 51: # Authentication Header
                ext_length = ((extension_header_length + 2) * 4)
            else:
                ext_length = ((extension_header_length + 1) * 8)

            if (len(data) < (offset + ext_length)):
                print(f"Incomplete {EXTENSION_HEADERS[next_header]} header, stopping.")
                break

            offset      += ext_length
            next_header  = next_header_pos

        self.header_size   = offset
        self.next_protocol = next_header