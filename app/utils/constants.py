import socket
hostname = socket.gethostname()

IGNORE_LOCALHOST = False # Because of WSL shenenigans, set it as True on windows
LOCALHOST        = '127.0.0.1'
NULL_MAC_ADDRESS = '00:00:00:00:00:00'

# If PC does not support IPv6, swap the lines
IPV6_ADDRESS = socket.getaddrinfo(hostname, None, socket.AF_INET6)
#IPV6_ADDRESS = ""
