import cv2

class V380:
    def __init__(self, ip, username, password):
        self.rtsp_url = f"rtsp://{username}:{password}@{ip}/live/ch00_0"
        self.cap = None

    def connect(self):
        self.cap = cv2.VideoCapture(self.rtsp_url)
        if not self.cap.isOpened():
            print(f"Error: Could not open video stream at {self.rtsp_url}")
            return False
        return True

    def get_frame(self):
        if self.cap is None or not self.cap.isOpened():
            if not self.connect():
                return None

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame from video stream.")
            return None
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()