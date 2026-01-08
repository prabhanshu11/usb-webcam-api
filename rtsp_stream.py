

import cv2
from v380 import V380
import time

# --- Configuration ---
CAMERA_IP = "192.168.29.251"
# Based on web search, default username is 'admin'
USERNAME = "admin"
# We will try with a blank password first, as it's the most common default.
PASSWORD = ""
OUTPUT_FILE = "rtsp_capture.jpg"

def capture_frame_from_rtsp():
    """Connects to the camera's RTSP stream and saves a single frame."""
    print(f"Attempting to connect to RTSP stream at: rtsp://{USERNAME}:<password>@{CAMERA_IP}/live/ch00_0")
    
    # Initialize the camera object from our v380.py library
    camera = V380(ip=CAMERA_IP, username=USERNAME, password=PASSWORD)

    # Connect to the stream
    if not camera.connect():
        print("Failed to connect. Please check the IP, username, and password.")
        # Try to release just in case it was partially opened
        camera.release()
        return

    print("Successfully connected to the RTSP stream.")

    # Give the stream a moment to stabilize
    time.sleep(1)

    # Get a single frame
    print("Capturing a frame...")
    frame = camera.get_frame()

    # Release the connection
    camera.release()
    print("Connection released.")

    if frame is not None:
        # Save the captured frame to a file
        try:
            cv2.imwrite(OUTPUT_FILE, frame)
            print(f"\nSUCCESS! Frame captured and saved to {OUTPUT_FILE}")
        except Exception as e:
            print(f"Error saving the frame: {e}", file=sys.stderr)
    else:
        print("Failed to capture a frame from the stream.")

if __name__ == "__main__":
    capture_frame_from_rtsp()

