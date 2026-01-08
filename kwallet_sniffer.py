import keyring
import subprocess

SERVICE_ID = "sudo"
PASSWORD = "iamapantar"

def run_sniffer():
    command = ["sudo", "-S", "/home/prabhanshu/Programs/usb-webcam-api/.venv/bin/python", "/home/prabhanshu/Programs/usb-webcam-api/sniffer.py"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = process.communicate(input=f"{PASSWORD}\n".encode())
    if process.returncode != 0:
        print(f"Error: {stderr.decode()}")

if __name__ == "__main__":
    run_sniffer()