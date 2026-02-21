import socket
import struct

def parse_header(data):
    # DNS Header is always 12 bytes
    # ! = Big-endian (Network Order)
    # H = Unsigned Short (2 bytes)
    # 6 H's = 12 bytes total
    header = struct.unpack("!HHHHHH", data[:12])
    
    return {
        "ID": header[0],
        "Flags": bin(header[1]),
        "QDCOUNT": header[2], # Question Count
        "ANCOUNT": header[3], # Answer Count
        "NSCOUNT": header[4], # Authority Count
        "ARCOUNT": header[5]  # Additional Count
    }

def start_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8053))
    print("🚀 Layer 1 & 2 Active: Listening on port 8053...")

    while True:
        data, addr = sock.recvfrom(512)
        print(f"\nIncoming packet from {addr}")
        
        header = parse_header(data)
        print(f"Header Parsed: {header}")
        
        # Layer 3 Preview: The raw 'Question' bytes after the header
        print(f"Raw Question Data: {data[12:].hex()}")

if __name__ == "__main__":
    start_listener()
