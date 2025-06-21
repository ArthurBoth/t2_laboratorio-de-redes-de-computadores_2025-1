from app.receivers.ethernet_receiver import EthernetReceiver
from app.receivers.network.arp_receiver import ARPReceiver
from app.receivers.network.ipv4_receiver import IPv4Receiver
from app.receivers.network.ipv6_receiver import IPv6Receiver
from app.receivers.transport_receiver import TransportReceiver

class ReceiverCreator:
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
    def transport(protocol: int) -> TransportReceiver | None:
        return TransportReceiver(protocol)