import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

s = socket.socket()
host = "192.168.1.109" # Server that is listening for the file.
port = 5001  # server's port number.
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))  # Make socket conn to host:port.
print("[+] Connected to ", host)
filename = input("File to Transfer : ")  # Add full path of file to send.
filesize = os.path.getsize(filename)  # Get size of file in bytes.
s.send(f"{filename}{SEPARATOR}{filesize}".encode()) # Send file over socket.

# Fancy progess bar.
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
# Read our file into the socket as bytes and update progess bar.
# As well as closing the client socket.
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()