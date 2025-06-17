from abc import ABC, abstractmethod

from app.receivers.ethernet_receiver import EthernetReceiver
from app.receivers.network.arp_receiver import ARPReceiver
from app.receivers.network.ipv4_receiver import IPv4Receiver
from app.receivers.network.ipv6_receiver import IPv6Receiver

class Receiver(ABC): 
    protocol_name: str
    eth_hex      : int
    header_index : int
    header_size  : int
    
    @staticmethod
    def data_link() -> EthernetReceiver:
        return EthernetReceiver()

    @staticmethod
    def network(hex_value: int) -> IPv4Receiver | IPv6Receiver | ARPReceiver | None:
        match hex_value:
            case 0x0800:
                return IPv4Receiver()
            case 0x86DD:
                return IPv6Receiver()
            case 0x0806:
                return ARPReceiver()
            case _:
                return None

    @staticmethod
    def transport(protocol: int) -> ICMPReceiver | TCPReceiver | UDPReceiver | None:
        match protocol:
            case 1, 58:  # ICMP, ICMPv6
                return ICMPReceiver(protocol)
            case 6:
                return TCPReceiver(protocol)
            case 17:
                return UDPReceiver(protocol)
            case _:
                return None
            
    def get_protocol_name(self) -> str:
        return self.protocol_name

    def assemble_return(self, timestamp, src_ip, dst_ip, protocol, total_len) -> list[str]:
        """Assemble the return string for CSV writing."""
        return [timestamp, self.protocol_name, src_ip, dst_ip, protocol, total_len]

    def get_header_index(self) -> int:
        """Return the index of the header in the data."""
        return self.header_index
    
    def get_header_size(self) -> int:
        """Return the size of the header."""
        return self.header_size
    
    @abstractmethod
    def get_protocol_data(self) -> int | None:
        """Return the protocol number."""
        pass

    @abstractmethod
    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        pass
