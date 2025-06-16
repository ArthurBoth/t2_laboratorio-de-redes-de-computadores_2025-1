import socket
from datetime import datetime
from collections import defaultdict
from app.receivers.network_receiver import NetworkReceiver
from csv_manager import CSVManager, OsiLayer

counters = defaultdict(int)

def main():
    sock    = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    manager = CSVManager()

    try:
        while True:
            raw_data = sock.recvfrom(1 << 16) # 64Kb buffer
            if (len(raw_data) < 14):
                continue

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            receiver  = NetworkReceiver.data_link()
            csv_list  = receiver.receive(timestamp, raw_data[0])

            if (not csv_list):
                continue
            manager.write(OsiLayer.DATA_LINK, csv_list)
            counters[receiver.get_protocol_name()] += 1

            receiver = NetworkReceiver.network(receiver.get_protocol_data())

            content = receiver.receive(raw_data[14:])
            if content:
                manager.write(receiver.get_protocol_name(), content)
                counters[receiver.get_protocol_name()] += 1
                print_counters()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        manager.close()
        sock.close()

def receive_ipv4(timestamp, data) -> bool:
    header    = struct.unpack('!BBHHHBBH4s4s', data[:20])
    total_len = header[2]
    protocol  = header[6]
    src_ip    = ip_format(header[8])
    dst_ip    = ip_format(header[9])

    if ((dst_ip == '127.0.0.1') or (src_ip == '127.0.0.1')):
        return True
    
    manager.write(OsiLayer.NETWORK, [timestamp, 'IPv4', src_ip, dst_ip, protocol, total_len])
    counters['IPv4'] += 1
    return False

def receive_arp(timestamp, data) -> bool:
    counters['ARP'] += 1
    return False

def receive_ipv6(timestamp, data) -> bool:
    counters['IPv6'] += 1
    return False

def print_counters():
    print('\r' + ' | '.join(f'{k}: {v}' for k, v in counters.items()), end='', flush=True)

if __name__ == '__main__':
    main()
