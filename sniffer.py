#!/home/prabhanshu/Programs/usb-webcam-api/.venv/bin/python
from scapy.all import sniff, IP, TCP, UDP

def packet_callback(packet):
    """
    This function is called for each captured packet.
    It prints a summary of the packet's information.
    """
    if IP in packet:
        ip_layer = packet[IP]
        proto = ip_layer.proto
        print(f"[+] New Packet: {ip_layer.src} -> {ip_layer.dst}")

        if proto == 6 and TCP in packet:
            tcp_layer = packet[TCP]
            print(f"    Protocol: TCP")
            print(f"    Source Port: {tcp_layer.sport}")
            print(f"    Destination Port: {tcp_layer.dport}")
            if raw_data := tcp_layer.payload:
                print(f"    Payload: {bytes(raw_data)}\n")

        elif proto == 17 and UDP in packet:
            udp_layer = packet[UDP]
            print(f"    Protocol: UDP")
            print(f"    Source Port: {udp_layer.sport}")
            print(f"    Destination Port: {udp_layer.dport}")
            if raw_data := udp_layer.payload:
                print(f"    Payload: {bytes(raw_data)}\n")

        else:
            print(f"    Protocol: Other ({proto})")
            if raw_data := ip_layer.payload:
                print(f"    Payload: {bytes(raw_data)}\n")

def main():
    """
    Main function to start the packet sniffer.
    """
    print("Starting packet sniffer...")
    # The prn argument specifies the callback function to be called for each packet
    # The store=False argument tells Scapy not to store the packets in memory
    sniff(prn=packet_callback, store=False)

if __name__ == "__main__":
    main()