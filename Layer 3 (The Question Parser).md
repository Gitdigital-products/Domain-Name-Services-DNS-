This is where the "magic" happens. In Layer 3, we have to decode the QNAME. DNS doesn't use dots (like google.com); it uses a sequence of labels.
Each label starts with a byte indicating its length, followed by that many characters. The sequence ends with a 00 byte (the null terminator).
🪜 Layer 3: The Label Decoder
To build this, we need a loop that reads one byte (the length), grabs that many characters, and repeats until it hits zero.
The Updated Script
Add this decode_labels function to your existing code to turn those hex bytes into a readable string:
def decode_labels(data, offset):
    labels = []
    while True:
        length = data[offset]
        if length == 0:  # End of the domain name
            offset += 1
            break
        
        offset += 1
        # Extract the label (e.g., 'google')
        label = data[offset : offset + length].decode("ascii")
        labels.append(label)
        offset += length
        
    return ".".join(labels), offset

# Update your listener to use it:
def start_listener_v2():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 8053))
    print("🚀 Layer 3 Active: Decoding Domain Names...")

    while True:
        data, addr = sock.recvfrom(512)
        
        # 1. Parse Header (Offset 0-12)
        header = parse_header(data)
        
        # 2. Parse Question (Starts at Offset 12)
        domain_name, next_offset = decode_labels(data, 12)
        
        # 3. Parse QTYPE and QCLASS (4 bytes total after the name)
        qtype, qclass = struct.unpack("!HH", data[next_offset : next_offset + 4])
        
        print(f"🔍 Query from {addr}: {domain_name} (Type: {qtype})")

🧩 What’s Happening Under the Hood?
 * The Pointer: We start at byte 12 (right after the header).
 * The Length Byte: If the first byte is 06, the code knows the next 6 bytes are part of the name.
 * The Type: After the name, the next 2 bytes tell us what kind of record they want.
   * Type 1 = A Record (IPv4 address)
   * Type 28 = AAAA Record (IPv6 address)
   * Type 15 = MX Record (Mail server)
🎯 Our Progress
We can now Receive a packet, Read the header, and Translate the domain name they are looking for.

 next step is the trickiest part of DNS: Label Length Encoding.
In the raw data, google.com looks like:
06 67 6f 6f 67 6c 65 03 63 6f 6d 00
(6 characters "google", 3 characters "com", ending in a null byte).