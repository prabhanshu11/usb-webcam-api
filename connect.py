import cv2
from v380 import V380

# Replace with your camera's IP address, username, and password
IP = "192.168.29.148"
PORT = 39985
USERNAME = "admin"
PASSWORD = ""

# Initialize the camera
camera = V380(IP, USERNAME, PASSWORD)
camera.rtsp_url = f"rtsp://{USERNAME}:{PASSWORD}@{IP}:{PORT}/live/ch00_0"

# Get a frame from the camera
frame = camera.get_frame()

if frame is not None:
    # Save the captured frame
    cv2.imwrite("capture.jpg", frame)
    print("Successfully captured an image from the camera!")
else:
    print("Failed to capture an image.")

camera.release()
