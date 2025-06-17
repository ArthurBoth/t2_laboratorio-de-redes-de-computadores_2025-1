from app.receivers.transport_receiver import TransportReceiver

class ICMPReceiver(TransportReceiver):
    def __init__(self, protocol: int):
        match protocol:
            case 1:
                self.protocol_name = "ICMP"
            case 58:
                self.protocol_name = "ICMPv6"
            case _:
                raise ValueError("Invalid ICMP protocol number")
            
    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        null = 0
        return self.assemble_return(timestamp, self.src_ip, null, self.dst_ip, null, len(data))
