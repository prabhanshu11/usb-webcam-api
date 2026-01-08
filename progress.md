Our primary goal is to reverse-engineer the network protocol of a V380 USB webcam to enable its RTSP stream.

**Key Discoveries & Challenges:**
*   Initial analysis of a pcap file showed the mobile app sends commands to the camera.
*   Simple replay failed, suggesting a dynamic session token is exchanged: the camera provides a token, which the app then uses in subsequent commands.
*   Attempts to create a handshake script (`send_command.py`) revealed a preliminary "hello" command (hex: `6a01...`) successfully initiates a session, leading to a 412-byte camera response.
*   The `v380.py` file indicated RTSP support, shifting our focus to enabling the RTSP server via the custom protocol.
*   Direct RTSP connection attempts failed, confirming the custom protocol is for authentication and activation.
*   A persistent "Connection reset by peer" error occurred, even when the mobile app was disconnected, suggesting the camera only accepts one connection at a time, or an issue with the handshake itself.
*   The `enable_rtsp_and_capture.py` script, designed to perform the full handshake and capture a frame, consistently extracted a suspicious `0000...` session token, which is likely incorrect.

**Current Status & Plan:**
*   We suspect the "Connection reset by peer" error and the invalid token are linked to an incorrect token extraction from the camera's 412-byte response.
*   To debug this, we need to accurately identify the real session token from the `camera_conversation.json` pcap analysis.
*   Due to the large size of `camera_conversation.json`, direct reading or searching was problematic.
*   **Current Action:** We successfully ran `parse_pcap.py` (a script designed to extract and filter payload data from the pcap JSON) with `--src-ip 192.168.29.251` and redirected its output to `/home/prabhanshu/Programs/usb-webcam-api/camera_responses.txt`. This was done to filter for camera responses specifically, avoid console overflow, and adhere to project directory constraints.
*   **Next Step:** Analyze the contents of `/home/prabhanshu/Programs/usb-webcam-api/camera_responses.txt` to locate the 412-byte response and correctly extract the dynamic session token.