import struct
from app.receivers.receiver import Receiver

class TransportReceiver(Receiver):
    protocol_id: int
    src_ip     : str
    dst_ip     : str
    unpack_str : str

    def __init__(self, protocol: int):
        self.protocol_id = protocol
        match protocol:
            case 1:
                self.protocol_name = "ICMP"
                self.header_size   = 8
            case 6:
                self.protocol_name = "TCP"
                self.header_size   = 20
                self.unpack_str    = "!HHLLBBHHH"
            case 17:
                self.protocol_name = "UDP"
                self.header_size   = 8
                self.unpack_str    = "!HHHH"
            case 58:
                self.protocol_name = "ICMPv6"
                self.header_size   = 4
            case _:
                raise ValueError(f"Unsuported protocol number: {protocol}")

    def set_ips(self, src_ip: str, dst_ip: str) -> None:
        """Set the source and destination IP addresses."""
        self.src_ip = src_ip
        self.dst_ip = dst_ip

    def assemble_return(self, timestamp, src_ip, src_port, dst_ip, dst_port, total_len) -> list[str]:
        """Assemble the return string for CSV writing."""
        return [timestamp, self.protocol_name, src_ip, src_port, dst_ip, dst_port, total_len]
    
    def get_protocol_data(self) -> int:
        """Return the protocol number."""
        return None

    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        if ((self.protocol_id == 1) or (self.protocol_id == 58)):
            src_port = 0
            dst_port = 0
        else:
            header = struct.unpack(self.unpack_str, data[:self.header_size])
            src_port = header[0]
            dst_port = header[1]

        return self.assemble_return(timestamp, self.src_ip, src_port, self.dst_ip, dst_port, len(data))
