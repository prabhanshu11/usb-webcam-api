

import socket
import sys
import time
import cv2
from v380 import V380 # We still use this for the final capture

# --- Configuration ---
CAMERA_IP = "192.168.29.251"
CAMERA_PORT = 8800 # The custom protocol port
USERNAME = "admin"
PASSWORD = "" # Assuming blank password for RTSP
OUTPUT_FILE = "final_capture.jpg"

# --- Command Templates ---
HELLO_CMD = bytes.fromhex("6a01000000000000000000000000000000000000000000000000000000000000")
CMD1_TEMPLATE = "6b010000d32239042a2c0000{token}0413120300000000000000000000000000000000000000000000000000000000000000000000000000000000"
CMD2_TEMPLATE = "6c0100000100c80000000000{token}041312000000000000000000"

def enable_rtsp_and_capture():
    """Performs the full handshake to enable the RTSP stream, then captures a frame."""
    try:
        # --- Part 1: Custom Protocol Handshake to Enable RTSP ---
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            print(f"Connecting to custom protocol at {CAMERA_IP}:{CAMERA_PORT}...")
            s.connect((CAMERA_IP, CAMERA_PORT))
            print("Connected. Sending HELLO...")
            s.sendall(HELLO_CMD)
            hello_response = s.recv(1024)
            if not hello_response or len(hello_response) < 20:
                print("Error: Did not receive a valid session token.", file=sys.stderr)
                return False
            
            # Extract the dynamic session token from the camera's response
            session_token = hello_response[8:20].hex()
            print(f"Received session token: {session_token}")

            # Build the two main commands with the dynamic token
            cmd1 = bytes.fromhex(CMD1_TEMPLATE.format(token=session_token))
            cmd2 = bytes.fromhex(CMD2_TEMPLATE.format(token=session_token))

            print("Sending Command 1 to enable stream...")
            s.sendall(cmd1)
            s.recv(1024) # Consume the confirmation response

            time.sleep(0.1)

            print("Sending Command 2 to finalize...")
            s.sendall(cmd2)
            s.recv(1024) # Consume the final confirmation

            print("RTSP stream should now be active.")
            # The handshake is complete. We can close this socket.

        # --- Part 2: Connect to the now-active RTSP Stream ---
        print("\nConnecting to the RTSP stream...")
        camera = V380(ip=CAMERA_IP, username=USERNAME, password=PASSWORD)
        if not camera.connect():
            print("Failed to connect to the RTSP stream after handshake.", file=sys.stderr)
            return False

        print("Successfully connected to RTSP. Capturing frame...")
        frame = camera.get_frame()
        camera.release()

        if frame is not None:
            cv2.imwrite(OUTPUT_FILE, frame)
            print(f"\nSUCCESS! Frame captured and saved to {OUTPUT_FILE}")
            return True
        else:
            print("Failed to capture frame from the active RTSP stream.", file=sys.stderr)
            return False

    except socket.error as e:
        print(f"A socket error occurred during the process: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    enable_rtsp_and_capture()
