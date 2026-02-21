At Layer 5, we move from a hardcoded response to a Data Store. A real DNS server doesn't have IPs written in its code; it looks them up in a Zone File.
We’ll implement a simple JSON-based "database" that allows your server to behave differently depending on the domain being requested.
📂 Layer 5: The Zone File (JSON Database)
A Zone File is essentially a dictionary where the Key is the domain and the Value contains the record details (Type, TTL, and IP).
1. Create your zones.json
Create a file in the same folder as your script:
{
    "example.com": {
        "A": "192.168.1.100",
        "ttl": 300
    },
    "google.com": {
        "A": "8.8.8.8",
        "ttl": 60
    },
    "mydev.local": {
        "A": "127.0.0.1",
        "ttl": 10
    }
}

🧠 2. The Lookup Logic
We need to update the build_response function to search this JSON file. If the domain isn't found, we should return an NXDOMAIN (Non-Existent Domain) error code so the client knows we don't have the answer.
The Updated Responder
import json

def load_zones():
    with open("zones.json") as f:
        return json.load(f)

def build_response_v2(data, domain_name):
    zones = load_zones()
    transaction_id = data[:2]
    
    # Check if domain exists in our "Database"
    if domain_name in zones:
        ip_address = zones[domain_name]["A"]
        ttl = zones[domain_name]["ttl"]
        flags = b'\x81\x80'  # Standard query response, No error
        ancount = b'\x00\x01'
    else:
        # If not found, send NXDOMAIN (Error Code 3)
        flags = b'\x81\x83'  
        ancount = b'\x00\x00'
        ip_address = None

    counts = b'\x00\x01' + ancount + b'\x00\x00\x00\x00'
    header = transaction_id + flags + counts

    # Question Section (Reused)
    _, offset = decode_labels(data, 12)
    question_section = data[12 : offset + 4]

    if ip_address:
        # Build Answer Section
        name_pointer = b'\xc0\x0c'
        type_class = b'\x00\x01\x00\x01'
        ttl_bytes = struct.pack("!I", ttl) # Encode TTL as 4-byte integer
        rd_length = b'\x00\x04'
        ip_bytes = socket.inet_aton(ip_address)
        
        answer_section = name_pointer + type_class + ttl_bytes + rd_length + ip_bytes
        return header + question_section + answer_section
    else:
        return header + question_section

🚀 The Result
Now, your server is Dynamic.
 * If you dig @127.0.0.1 -p 8053 example.com, you get 192.168.1.100.
 * If you dig @127.0.0.1 -p 8053 unknown.com, you get an "ANSWER: 0" and an NXDOMAIN status.
🧗 Layer 6: Recursive Forwarding (The "Real" Internet)
Currently, your server only knows what's in your JSON file. If it doesn't know the answer, it just gives up.

