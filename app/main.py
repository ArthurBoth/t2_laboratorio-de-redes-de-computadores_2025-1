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
            csv_list = receiver.receive(timestamp, raw_data[receiver.header_index:])
            if (not csv_list):
                continue
            manager.write(OsiLayer.NETWORK, csv_list)
            counters[receiver.get_protocol_name()] += 1

            receiver = NetworkReceiver.transport(receiver.get_protocol_data())
            csv_list = receiver.receive(timestamp, raw_data[receiver.header_index:])
            if (not csv_list):
                continue
            manager.write(OsiLayer.TRANSPORT, csv_list)
            counters[receiver.get_protocol_name()] += 1

            print_counters()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        manager.close()
        sock.close()

def print_counters():
    print('\r' + ' | '.join(f'{k}: {v}' for k, v in counters.items()), end='', flush=True)

if __name__ == '__main__':
    main()
