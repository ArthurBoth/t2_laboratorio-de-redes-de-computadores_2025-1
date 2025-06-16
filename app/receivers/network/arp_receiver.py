import struct

from app.utils import formatter
from ..network_receiver import NetworkReceiver

PTYPE_NAMES = {
    0x0800: "IPv4",
    0x0806: "ARP",
    0x8035: "RARP",
    0x809B: "AppleTalk",
    0x8137: "IPX",
    0x86DD: "IPv6",
    0x880B: "PPP",
    0x8847: "MPLS Unicast",
    0x8848: "MPLS Multicast",
}

class ARPReceiver(NetworkReceiver):
    next_protocol: int

    def __init__(self):
        self.protocol_name        = "ARP"
        self.header_index         = 14
        self.header_size          = 28
        self.constant_header_size = 8

    def receive(self, timestamp, data) -> str:
        """Process the received data and return a string list, ready to be written to CSV."""

        _, protocol_type, hw_size, proto_size, _ = struct.unpack('!HHBBH', data[:self.constant_header_size])

        start = self.constant_header_size + hw_size

        src_ip = formatter.dynamic_protocol_format(protocol_type, data[start:start+proto_size])
        start += proto_size + hw_size
        dst_ip = formatter.dynamic_protocol_format(protocol_type, data[start:start+proto_size])

        protocol_subname   = PTYPE_NAMES.get(protocol_type, f"Unknown Protocol {protocol_type:#04x}")

        return self.assemble_return(timestamp, src_ip, dst_ip, protocol_subname, self.header_size)

    def get_protocol_data(self) -> int:
        """Return the next_protocol number."""
        return self.next_protocol
