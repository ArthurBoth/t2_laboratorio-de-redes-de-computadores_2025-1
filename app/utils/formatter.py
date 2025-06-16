def mac_format(mac_bytes):
    return ':'.join(f'{b:02x}' for b in mac_bytes)

def ip_format(ip_bytes):
    return '.'.join(str(b) for b in ip_bytes)