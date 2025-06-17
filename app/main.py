import socket
from datetime import datetime
from collections import defaultdict
from app.receivers.receiver import Receiver
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

            receiver = Receiver.data_link()
            csv_list = receiver.receive(timestamp, raw_data[0])
            if (not csv_list):
                continue
            manager.write(OsiLayer.DATA_LINK, csv_list)
            counters[receiver.get_protocol_name()] += 1

            receiver        = Receiver.network(receiver.get_protocol_data())
            nt_header_index = receiver.get_header_index()
            nt_header_size  = receiver.get_header_size()
            csv_list        = receiver.receive(timestamp, raw_data[nt_header_index:])
            if (not csv_list):
                continue
            manager.write(OsiLayer.NETWORK, csv_list)
            counters[receiver.get_protocol_name()] += 1

            receiver = Receiver.transport(receiver.get_protocol_data())
            if (not receiver):
                continue
            receiver.set_ips(csv_list[2], csv_list[3])
            csv_list = receiver.receive(timestamp, raw_data[(nt_header_index + nt_header_size):])
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
