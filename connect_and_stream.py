
import socket
import sys
import time

# --- Configuration ---
CAMERA_IP = "192.168.29.251"
CAMERA_PORT = 8800
OUTPUT_FILE = "camera_feed.jpeg"

# --- Command Templates (as hex strings) ---

# 1. The initial "hello" command to start a new session.
HELLO_COMMAND_HEX = "6a01000000000000000000000000000000000000000000000000000000000000"

# 2. Template for the first main command (originally the 'k' command).
# The {token} will be replaced by the bytes we get from the camera's hello response.
MAIN_COMMAND_1_TEMPLATE_HEX = "6b010000d32239042a2c0000{token}0413120300000000000000000000000000000000000000000000000000000000000000000000000000000000"

# 3. Template for the second main command (originally the 'l' command).
# This also uses the same session token.
MAIN_COMMAND_2_TEMPLATE_HEX = "6c0100000100c80000000000{token}041312000000000000000000"


def get_live_feed():
    """Performs the full, stateful handshake to request the video feed."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            print(f"Connecting to {CAMERA_IP}:{CAMERA_PORT}...")
            s.connect((CAMERA_IP, CAMERA_PORT))
            print("Connected.")

            # --- Step 1: Send HELLO to get a session token ---
            print("Sending HELLO command...")
            s.sendall(bytes.fromhex(HELLO_COMMAND_HEX))
            hello_response = s.recv(1024)
            if not hello_response or len(hello_response) < 20:
                print("Error: Did not receive a valid session token.", file=sys.stderr)
                return
            print(f"Received session response ({len(hello_response)} bytes).")

            # --- Step 2: Extract the session token ---
            # From analyzing the pcap, the token seems to be a recurring block.
            # Let's hypothesize it's the 12 bytes starting at offset 8.
            session_token_bytes = hello_response[8:20]
            session_token_hex = session_token_bytes.hex()
            print(f"Extracted Session Token: {session_token_hex}")

            # --- Step 3: Build and send the two main commands ---
            cmd1_hex = MAIN_COMMAND_1_TEMPLATE_HEX.format(token=session_token_hex)
            cmd2_hex = MAIN_COMMAND_2_TEMPLATE_HEX.format(token=session_token_hex)
            cmd1_bytes = bytes.fromhex(cmd1_hex)
            cmd2_bytes = bytes.fromhex(cmd2_hex)

            print("Sending Main Command 1...")
            s.sendall(cmd1_bytes)
            confirmation = s.recv(1024)
            print(f"Received confirmation: {confirmation.hex()}")

            time.sleep(0.1)

            print("Sending Main Command 2...")
            s.sendall(cmd2_bytes)

            # --- Step 4: Listen for the video stream ---
            print(f"Listening for video stream... saving to {OUTPUT_FILE}")
            s.settimeout(10)
            video_data = b''
            try:
                while True:
                    chunk = s.recv(8192)
                    if not chunk:
                        break
                    video_data += chunk
            except socket.timeout:
                print("Finished receiving data.")

            if video_data:
                jpeg_start = video_data.find(b'\xff\xd8\xff')
                if jpeg_start != -1:
                    jpeg_data = video_data[jpeg_start:]
                    with open(OUTPUT_FILE, 'wb') as f:
                        f.write(jpeg_data)
                    print(f"SUCCESS! Image saved to {OUTPUT_FILE}")
                else:
                    print("Could not find JPEG header. Saving raw stream.")
                    with open("raw_stream.dat", 'wb') as f:
                        f.write(video_data)
            else:
                print("No video data received.")

    except socket.error as e:
        print(f"Socket error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    get_live_feed()
