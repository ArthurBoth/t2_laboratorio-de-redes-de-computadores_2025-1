import struct

from app.receivers.transport_receiver import TransportReceiver

class TCPReceiver(TransportReceiver):
    def __init__(self):
        self.protocol_name = "TCP"
        self.header_size   = 20

    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        header = struct.unpack('!HHLLBBHHH', data[:self.header_size])
        src_port = header[0]
        dst_port = header[1]

        return self.assemble_return(timestamp, self.src_ip, src_port, self.dst_ip, dst_port, len(data))
