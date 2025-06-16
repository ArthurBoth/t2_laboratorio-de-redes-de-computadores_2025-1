import socket
import struct
from datetime import datetime
from collections import defaultdict
from csv_manager import CSVManager, OsiLayer

counters = defaultdict(int)

def mac_format(mac_bytes):
    return ':'.join(f'{b:02x}' for b in mac_bytes)

def ip_format(ip_bytes):
    return '.'.join(str(b) for b in ip_bytes)

def main():
    sock     = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    manager  = CSVManager()

    try:
        while True:
            raw_data = sock.recvfrom(1 << 12) # 4Kb buffer
            if len(raw_data) < 14:
                continue

            timestamp     = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            ethernet_data = struct.unpack('!6s6sH', raw_data[0:14])
            dest_mac      = mac_format(ethernet_data[0])
            src_mac       = mac_format(ethernet_data[1])
            eth_protocol  = ethernet_data[2]
            total_len     = len(raw_data)

            manager.write(OsiLayer.DATA_LINK, [timestamp, src_mac, dest_mac, hex(eth_protocol), total_len])
            counters['Ethernet'] += 1

            match eth_protocol:
                case 0x0800:
                    receive_ipv4(raw_data[14:34])
                case 0x0806:
                    receive_arp(raw_data[14:28])
                case 0x86DD:
                    receive_ipv6(raw_data[14:34])
                case _:
                    counters[f'OUTRO_{hex(eth_protocol)}'] += 1

            print_counters()

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    finally:
        manager.close()
        sock.close()

def receive_ipv4(data):
    counters['IPv4'] += 1

def receive_arp(data):
    counters['ARP'] += 1

def receive_ipv6(data):
    counters['IPv6'] += 1

def print_counters():
    print('\r' + ' | '.join(f'{k}: {v}' for k, v in counters.items()), end='', flush=True)

if __name__ == '__main__':
    main()
