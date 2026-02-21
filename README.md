Done! Let’s wrap this up in Docker. This is the "Pro" move—it ensures your DNS server has a consistent environment, handles its own dependencies, and can be easily deployed on a Raspberry Pi, a home server, or a VPS.
Since DNS usually requires Port 53, Docker helps us manage that mapping cleanly.
🐳 Dockerizing the DNS Service
1. The Dockerfile
This tells Docker how to package your Python script. We'll use a "slim" image to keep it lightweight.
# Use a tiny Python footprint
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your script and your zone file
COPY main.py .
COPY zones.json .

# DNS runs on UDP port 53
EXPOSE 53/udp

# Run the server
CMD ["python", "main.py"]

2. The docker-compose.yml
This makes it easy to manage the container, especially if you want it to restart automatically if it crashes.
services:
  dns-server:
    build: .
    container_name: custom-dns
    ports:
      - "53:8053/udp" # Map host port 53 to our app's port 8053
    volumes:
      - ./zones.json:/app/zones.json # Sync zones so you can edit without rebuilding
    restart: always

🚀 Deployment
To launch your service, just run:
docker-compose up -d

Your server is now running in the background. You can edit zones.json on your host machine, and the container will see the changes (if your Python script re-reads the file per query).
🛡️ The Final Badge Wall
To make your GitHub profile pop, add this section to the very top of your README.md. It gives it that "Enterprise Tool" aesthetic.
# 🌐 Domain-Name-Services-DNS-

<p align="center">
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/Architecture-Recursive-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Traffic-UDP-orange?style=for-the-badge" />
</p>

---

💡 Pro Tip: Ad-Blocking
Since you control the zones.json, you can now perform DNS Sinkholing. If you add an entry for doubleclick.net and point it to 0.0.0.0, any device using your DNS server will effectively block those ads at the network level.
Would you like me to generate a script that automatically imports a "Blocklist" of 10,000+ known ad domains into your zones.json?
 README.md for your project.
🌐 Custom DNS Service (Layer-by-Layer)
A high-performance, lightweight DNS resolver built from the ground up. This project avoids heavy libraries to demonstrate the core binary mechanics of the Domain Name System, including packet parsing, label decoding, and recursive forwarding.
🏗️ Architectural Layers
This repository follows a 6-layer construction methodology:
 * Layer 1: UDP Transport – Low-level socket management on Port 53/8053.
 * Layer 2: Binary Header Parser – Unpacking the 12-byte DNS header (IDs, Flags, Counts).
 * Layer 3: Label Decoder – Converting hex-encoded labels (e.g., 03www06google03com) into strings.
 * Layer 4: Response Constructor – Manually crafting binary response packets and bit-flipping flags.
 * Layer 5: Data Store (Zone Files) – A JSON-based database for local domain overrides.
 * Layer 6: Recursive Resolver – Automated forwarding to upstream providers (8.8.8.8) for unknown queries.
🚀 Getting Started
Prerequisites
 * Python 3.9+
 * dig or nslookup for testing
Installation
git clone https://github.com/Gitdigital-products/Domain-Name-Services-DNS-
cd Domain-Name-Services-DNS-

Running the Server
To run on the default DNS port (53), you may need sudo/admin privileges:
python3 main.py

🧪 Testing
Use dig to verify both local and recursive lookups:
Local Lookup (Zone File):
dig @127.0.0.1 -p 8053 mydev.local

Recursive Lookup (The Internet):
dig @127.0.0.1 -p 8053 google.com

📂 Configuration (zones.json)
Manage your local records by editing the zones.json file:
{
    "example.local": {
        "A": "1.2.3.4",
        "ttl": 300
    }
}

🛠️ Built With
 * Python Standard Library – No external dependencies for core logic.
 * Struct & Socket – For binary manipulation and network transport.

Domain Name Services (DNS):** Decentralized domain name resolution
