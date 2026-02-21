// Listen on UDP port 8053
conn, _ := net.ListenUDP("udp", &net.UDPAddr{Port: 8053})
defer conn.Close()

buffer := make([]byte, 512) // DNS packets are usually max 512 bytes
n, addr, _ := conn.ReadFromUDP(buffer)

fmt.Printf("Received %d bytes from %s\n", n, addr)
