import json
import sys
import argparse
from collections import Counter

def parse_pcap_json(filename, src_ip=None, max_len=None, unique=False, length=None):
    """
    Parses the tshark JSON output, filtering for specific packets and optionally
    showing unique payloads.
    """
    try:
        with open(filename, 'r') as f:
            packets = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filename}: {e}", file=sys.stderr)
        return
    except FileNotFoundError:
        print(f"Error: File not found at {filename}", file=sys.stderr)
        return

    payloads = []

    for packet in packets:
        try:
            layers = packet.get("_source", {}).get("layers", {})

            # --- Filtering --- 
            current_ip_src = layers.get("ip", {}).get("ip.src")
            if src_ip and current_ip_src != src_ip:
                continue

            payload = None
            if "data" in layers:
                payload = layers.get("data", {}).get("data.data")
            # The V380 protocol seems to use a custom protocol on top of TCP.
            # tshark might label this as just "data" or a specific protocol if it understands it.
            # Let's check for a known V380 protocol layer if one exists, otherwise stick to "data".
            elif "v380" in layers: # Hypothetical protocol name
                 payload = layers.get("v380",{}).get("v380.data")
            elif "tcp" in layers and layers["tcp"].get("tcp.payload"):
                payload = layers["tcp"].get("tcp.payload")

            if not payload:
                continue

            payload_bytes = bytes.fromhex(payload.replace(":", ""))

            if max_len and len(payload_bytes) > max_len:
                continue

            if length and len(payload_bytes) != length:
                continue
            
            # --- Data Extraction --- 
            frame_time = layers.get("frame", {}).get("frame.time_relative")
            ip_dst = layers.get("ip", {}).get("ip.dst")
            tcp_srcport = layers.get("tcp", {}).get("tcp.srcport")
            tcp_dstport = layers.get("tcp", {}).get("tcp.dstport")

            output_data = {
                "time": frame_time,
                "source": f"{current_ip_src}:{tcp_srcport}",
                "destination": f"{ip_dst}:{tcp_dstport}",
                "payload_bytes": repr(payload_bytes)
            }
            payloads.append(output_data)

        except (KeyError, AttributeError):
            # Skip packets that don't have the fields we need
            continue

    if unique:
        # Group by unique payload and show counts and timings
        unique_payloads = Counter(p["payload_bytes"] for p in payloads)
        for payload, count in unique_payloads.items():
            # Find the first time this payload appeared
            first_occurrence = next((p for p in payloads if p["payload_bytes"] == payload), None)
            print(f"Count: {count}, First seen at: {first_occurrence['time']}s")
            print(f"  Source: {first_occurrence['source']}")
            print(f"  Payload (raw bytes): {payload}")
            print("-" * 40)
    else:
        for p in payloads:
            print(f"Time: {p['time']}, {p['source']} -> {p['destination']}")
            print(f"  Payload (raw bytes): {p['payload_bytes']}")
            print("-" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse and filter tshark JSON output to find command payloads.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "filename", 
        help="Path to the camera_conversation.json file."
    )
    parser.add_argument(
        "--src-ip", 
        help="Filter by source IP address (e.g., the phone's IP)."
    )
    parser.add_argument(
        "--max-len", 
        type=int, 
        help="Only show payloads with a size up to max_len bytes (e.g., 100)."
    )
    parser.add_argument(
        "--unique", 
        action="store_true", 
        help="Show only unique payloads and their counts."
    )
    parser.add_argument(
        "--len", 
        type=int, 
        help="Only show payloads with a size equal to len bytes."
    )
    
    args = parser.parse_args()

    parse_pcap_json(args.filename, args.src_ip, args.max_len, args.unique, args.len)