
import socket
import sys

# --- Configuration ---
CAMERA_IP = "192.168.29.251"
CAMERA_PORT = 8800

# This is the simple "hello" command sent by the app at the beginning of a session.
# We will send this to see how the camera responds and if it gives us a session token.
HELLO_COMMAND_HEX = "6a01000000000000000000000000000000000000000000000000000000000000"

def send_hello():
    """Sends the simple initial command and prints the camera's response."""
    payload = bytes.fromhex(HELLO_COMMAND_HEX)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            print(f"Connecting to {CAMERA_IP}:{CAMERA_PORT}...")
            s.connect((CAMERA_IP, CAMERA_PORT))
            print("Connected.")

            # --- Send the "hello" command ---
            print(f"Sending hello command: {repr(payload)}")
            s.sendall(payload)

            # --- Listen for the response ---
            response = s.recv(1024)
            if response:
                print(f"SUCCESS: Received a response ({len(response)} bytes).")
                print(f"Response (hex): {response.hex()}")
            else:
                print("No response received from camera.")

    except socket.error as e:
        print(f"Socket error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    send_hello()
