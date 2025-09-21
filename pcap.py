from scapy.all import rdpcap


pcap_file = "example.pcap"


packets = rdpcap(pcap_file)

print(f"Total packets: {len(packets)}\n")

for i, pkt in enumerate(packets, 1):
    print(f"Packet {i}:")
    print(pkt.summary())  
    print(pkt.show(dump=True)) 
    print("-"*50)
