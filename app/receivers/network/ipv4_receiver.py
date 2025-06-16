import struct

from app.utils import formatter
from ..network_receiver import NetworkReceiver

class IPv4Receiver(NetworkReceiver):
    def __init__(self):
        self.protocol_name = "IPv4"

    def receive(self, timestamp, data) -> str:
        """Process the received data and return a string list, ready to be written to CSV."""
        header    = struct.unpack('!BBHHHBBH4s4s', data[:20])
        total_len = header[2]
        protocol  = header[6]
        src_ip    = formatter.ip_format(header[8])
        dst_ip    = formatter.ip_format(header[9])

        if ((dst_ip == '127.0.0.1') or (src_ip == '127.0.0.1')):
            return ''
        return self.assemble_return(timestamp, src_ip, dst_ip, protocol, total_len)