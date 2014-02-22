
import streamy
import sys
import socket

if __name__ == "__main__":
    if len(sys.argv) == 1:
        ip_addr = socket.gethostbyname(socket.getfqdn())
        streamy.run(ip_addr, 8000)
    elif len(sys.argv) == 3:
        streamy.run(sys.argv[1], int(sys.argv[2]))
