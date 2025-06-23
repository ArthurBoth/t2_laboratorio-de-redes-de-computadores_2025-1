from abc import ABC, abstractmethod

class Receiver(ABC): 
    protocol_name: str
    eth_hex      : int
    header_index : int
    header_size  : int
            
    def get_protocol_name(self) -> str:
        return self.protocol_name

    def get_header_index(self) -> int:
        """Return the index of the header in the data."""
        return self.header_index
    
    def get_header_size(self) -> int:
        """Return the size of the header."""
        return self.header_size

    @abstractmethod
    def assemble_return(self, timestamp, src, dst, protocol, total_len) -> list[str]:
        """Assemble the return string for CSV writing."""
        pass
    
    @abstractmethod
    def get_protocol_data(self) -> int | None:
        """Return the protocol number."""
        pass

    @abstractmethod
    def receive(self, timestamp: str, data: bytes) -> list:
        """Process the received data and return a string list, ready to be written to CSV."""
        pass
