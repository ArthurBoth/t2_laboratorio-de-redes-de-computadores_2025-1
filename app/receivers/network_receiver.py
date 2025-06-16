from abc import ABC, abstractmethod

from app.receivers.ethernet_receiver import EthernetReceiver
from app.receivers.network.ipv4_receiver import IPv4Receiver

class NetworkReceiver(ABC):
    protocol_name: str
    eth_hex: int
    
    @staticmethod
    def data_link() -> EthernetReceiver:
        return EthernetReceiver()

    @staticmethod
    def network(hex_value):
        if hex_value == 0x0800:
            return IPv4Receiver()
        elif hex_value == 0x86DD:
            return IPv6Receiver()
        elif hex_value == 0x0806:
            return ARPReceiver()
        else:
            return OtherReceiver(hex_value)
        
    @staticmethod
    def transport():
        pass

    def get_protocol_name(self) -> str:
        return self.protocol_name

    def assemble_return(self, timestamp, src_ip, dst_ip, protocol, total_len) -> str:
        """Assemble the return string for CSV writing."""
        return [timestamp, self.protocol_name, src_ip, dst_ip, protocol, total_len]
    
    @abstractmethod
    def get_protocol_data(self) -> int:
        """Return the protocol number."""
        pass

    @abstractmethod
    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        pass
