def mac_format(mac_bytes: bytes) -> str:
    return ':'.join(f'{b:02x}' for b in mac_bytes)

def ipv4_format(ip_bytes: bytes) -> str:
    return '.'.join(str(b) for b in ip_bytes)

def ipv6_format(ip_bytes: bytes) -> str:
    return ':'.join(f'{(ip_bytes[i] << 8 | ip_bytes[i+1]):x}' for i in range(0, 16, 2))

def unknown_format(protocol_bytes: bytes) -> str:
    return '0x' + protocol_bytes.hex()

def dynamic_protocol_format(protocol_type, proto_bytes):
    if ((protocol_type == 0x0800) and (len(proto_bytes) == 4)):
        return ipv4_format(proto_bytes)
    elif ((protocol_type == 0x86DD) and (len(proto_bytes) == 16)):
        return ipv6_format(proto_bytes)
    else:
        return unknown_format(proto_bytes)
