# Context Transfer Prompt for V380 USB Webcam API Project

**Copy everything below this line and paste as your first message in a new Claude Code session started from ~/Programs/usb-webcam-api:**

---

## Resume: V380 USB Webcam Protocol Reverse Engineering

I was working on reverse-engineering the V380 USB webcam's network protocol to enable RTSP video streaming. The previous conversation got corrupted due to too many screenshots. Here's where we left off:

### Project Goal
Reverse-engineer the custom binary protocol used by V380 camera to authenticate and enable RTSP streaming.

### What's Been Completed
1. **PCAP Analysis**: Captured network traffic between V380 mobile app and camera using PCAPdroid
2. **Protocol Discovery**: Identified a custom binary protocol (not standard RTSP) for authentication
3. **Initial Handshake**: Discovered the "hello" command in hex format (`6a01...`) successfully initiates a session - camera responds with 412 bytes
4. **Scripts Created**:
   - `send_command.py` - Initial handshake implementation
   - `enable_rtsp_and_capture.py` - Full handshake + frame capture attempt
   - `parse_pcap.py` - PCAP JSON parsing/filtering script
   - `v380.py` - OpenCV-based RTSP streaming class
   - `connect.py` - Connection management

### Current Blocker
The `enable_rtsp_and_capture.py` script extracts an invalid session token (`0000...` values), causing "Connection reset by peer" errors.

Two hypotheses:
1. Camera accepts only ONE connection at a time
2. Incorrect token extraction from the 412-byte camera response

### Last Action Taken
Ran `parse_pcap.py` with `--src-ip 192.168.29.251` to filter camera responses, output saved to:
- `/home/prabhanshu/Programs/usb-webcam-api/camera_responses.txt`

### Immediate Next Step
Analyze `camera_responses.txt` to locate the 412-byte response and correctly identify where the dynamic session token is within that response.

### Key Technical Details
- **Camera IP**: 192.168.29.251
- **RTSP URL Format**: `rtsp://{username}:{password}@{ip}/live/ch00_0`
- **Protocol**: Custom binary authentication, then standard RTSP
- **Hello command**: `6a01...` (hex)
- **Expected response**: 412 bytes containing session token

### Important Files
- `camera_conversation.json` - Full PCAP analysis
- `camera_responses.txt` - Filtered camera responses (analyze this next)
- `412_byte_responses.txt` - Previously extracted responses
- `PCAPdroid_26_Jun_03_24_46.pcap` - Raw PCAP file

### Continue With
Please analyze `camera_responses.txt` to find the 412-byte response and help me identify the correct byte offset for the session token extraction.
