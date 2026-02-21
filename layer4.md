Layer 4 is the most rewarding part: The Response. This is where we stop just listening and start acting like a real server.
To do this, we have to construct a packet that mirrors the question but adds an Answer Section. This section tells the client, "Yes, I found google.com, and here is its IP address."
🛠️ Layer 4: Constructing the Answer
A DNS Answer has a specific binary structure. If we want to point a domain to 127.0.0.1, we have to encode that IP into 4 bytes: \x7f\x00\x00\x01.
The Logic:
 * Modify the Header: Change the "QR" (Query/Response) bit to 1 and set ANCOUNT (Answer Count) to 1.
 * Keep the Question: You must repeat the question exactly as it was sent to you.
 * Append the Answer: Use a "Pointer" (0xc00c) to save space by pointing back to the domain name in the question section, then provide the IP.
📝 The "Responder" Code
Add this function to your script to build the binary response:
def build_response(data, domain_name, ip_address="127.0.0.1"):
    # 1. Header: Copy ID, Set Flags to 0x8180 (Standard Response), 
    # Questions=1, Answers=1, Auth=0, Addit=0
    transaction_id = data[:2]
    flags = b'\x81\x80'
    counts = b'\x00\x01\x00\x01\x00\x00\x00\x00'
    header = transaction_id + flags + counts

    # 2. Question: We reuse the question section from the original request
    # (From byte 12 until the end of the QTYPE/QCLASS)
    # Finding where the question ends:
    _, offset = decode_labels(data, 12)
    question_section = data[12 : offset + 4]

    # 3. Answer: 
    # Name Pointer (0xc00c points to the name at offset 12)
    # Type A (0x0001), Class IN (0x0001), TTL 60s (0x0000003c)
    # Data Length 4 (0x0004), IP Address (4 bytes)
    name_pointer = b'\xc0\x0c'
    type_class_ttl = b'\x00\x01\x00\x01\x00\x00\x00\x3c'
    rd_length = b'\x00\x04'
    
    # Convert "127.0.0.1" to bytes
    ip_bytes = socket.inet_aton(ip_address)
    
    answer_section = name_pointer + type_class_ttl + rd_length + ip_bytes
    
    return header + question_section + answer_section

🚀 The Full Loop
Now, update your while True loop to send the data back:
        # ... (after parsing the domain name) ...
        
        response = build_response(data, domain_name, "1.2.3.4") # Pick any IP!
        sock.sendto(response, addr)
        print(f"✅ Sent response for {domain_name} -> 1.2.3.4")

🧪 Testing the "Fake" DNS
 * Run your updated script.
 * In your terminal, run:
   dig @127.0.0.1 -p 8053 mysite.com
 * The Result: dig will report that mysite.com is at 1.2.3.4. You have officially hijacked a local DNS query!
🏢 Layer 5: The Data Store (The "Zone File")
Hardcoding IPs is fine for a lab, but a real server needs a "Brain."
