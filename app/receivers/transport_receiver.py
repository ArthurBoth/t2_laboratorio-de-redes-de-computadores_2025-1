from app.receivers.receiver import Receiver


class TransportReceiver(Receiver):
    src_ip: str
    dst_ip: str

    def __init__(self, protocol: int):
        self.protocol = protocol

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

    @abstractmethod
    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        pass
