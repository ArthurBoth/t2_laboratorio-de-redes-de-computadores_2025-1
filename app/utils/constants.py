import socket
hostname = socket.gethostname()

IGNORE_LOCALHOST = False
IPV6_ADDRESS     = socket.getaddrinfo(hostname, None, socket.AF_INET6)
LOCALHOST        = '127.0.0.1'
NULL_MAC_ADDRESS = '00:00:00:00:00:00'