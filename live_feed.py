import cv2
import time

# --- User Configuration ---
# Replace this with your camera's IP address
IP_ADDRESS = "192.168.29.148"  # <--- CHANGE THIS TO YOUR CAMERA'S IP

# These are common defaults, but you may need to find the correct ones
USERNAME = "admin"
PASSWORD = ""  # Many V380 cameras have a blank password by default
RTSP_PATH = "live/ch00_0" # This is a common path, but might be different (e.g., live/ch00_1, video.sdp)
# --- End Configuration ---


# --- Main Application ---
def main():
    """
    Connects to the camera's RTSP stream and displays the live feed.
    """
    # The RTSP (Real Time Streaming Protocol) URL is how we connect to the video feed.
    rtsp_url = f"rtsp://{USERNAME}:{PASSWORD}@{IP_ADDRESS}/{RTSP_PATH}"
    
    print(f"Attempting to connect to: {rtsp_url}")

    # Loop to continuously try reconnecting if the stream fails
    while True:
        # Open the video stream
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            print("Error: Could not open video stream. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        print("Successfully connected to camera. Displaying feed.")
        print("Press 'q' in the video window to quit.")

        # Read and display frames from the stream
        while True:
            ret, frame = cap.read()
            
            # If we failed to get a frame, the connection might be lost.
            # Break the inner loop to try reconnecting.
            if not ret:
                print("Error: Lost connection to the stream. Reconnecting...")
                break
            
            # Display the resulting frame
            cv2.imshow('V380 Camera Live Feed', frame)

            # Wait for 1ms and check if the user pressed 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Break both loops to exit the program
                cap.release()
                cv2.destroyAllWindows()
                print("Stream stopped by user.")
                return
        
        # Release the capture object before trying to reconnect
        cap.release()
        time.sleep(1) # Brief pause before reconnection attempt

if __name__ == "__main__":
    main()
