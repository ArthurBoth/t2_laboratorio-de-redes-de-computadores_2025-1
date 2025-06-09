# This is AI generated code, used for testing whether windows can run Python raw sockets.

import socket
import struct
import threading
import sys

running = True

def listen_dhcp():
    global running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 67))
    print("Listening for DHCP packets on UDP port 67... (type 'exit' to stop)")

    while running:
        try:
            sock.settimeout(1.0)  # So we can check `running` periodically
            data, addr = sock.recvfrom(1024)

            print(f"\nReceived {len(data)} bytes from {addr}")

            if len(data) < 240:
                print("Not a valid DHCP packet (too short).")
                continue

            bootp = struct.unpack('!BBBBIHHIIII16s64s128s', data[:236])

            op = bootp[0]
            xid = bootp[4]
            chaddr = bootp[10][:6]
            mac = ':'.join(f'{b:02x}' for b in chaddr)

            print(f"OP: {op} (1=request, 2=reply)")
            print(f"Transaction ID: {xid:#x}")
            print(f"Client MAC: {mac}")

            if data[236:240] != b'\x63\x82\x53\x63':
                print("No DHCP magic cookie found.")
                continue

            options = data[240:]
            i = 0
            while i < len(options):
                opt = options[i]
                if opt == 255:
                    break
                elif opt == 0:
                    i += 1
                    continue
                length = options[i + 1]
                value = options[i + 2:i + 2 + length]

                if opt == 53:
                    msg_type = value[0]
                    types = {
                        1: "DHCPDISCOVER",
                        2: "DHCPOFFER",
                        3: "DHCPREQUEST",
                        4: "DHCPDECLINE",
                        5: "DHCPACK",
                        6: "DHCPNAK",
                        7: "DHCPRELEASE",
                        8: "DHCPINFORM"
                    }
                    print(f"DHCP Message Type: {msg_type} ({types.get(msg_type, 'Unknown')})")

                i += 2 + length

        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error: {e}")
            break

    print("Stopping DHCP listener...")
    sock.close()

def wait_for_exit():
    global running
    while True:
        user_input = input()
        if user_input.strip().lower() == 'exit':
            running = False
            break

if __name__ == "__main__":
    threading.Thread(target=wait_for_exit, daemon=True).start()
    try:
        listen_dhcp()
    except KeyboardInterrupt:
        running = False
        print("\nInterrupted by user.")
