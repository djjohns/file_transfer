import socket
import tqdm
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()  # Create our socket.
s.bind((SERVER_HOST, SERVER_PORT))  # Bind it to our host:port.
s.listen(10)  # Listen for a connection.
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
print("Waiting for the client to connect... ")
client_socket, address = s.accept()  # Accept the connection.
print(f"[+] {address} is connected.")
received = client_socket.recv(BUFFER_SIZE).decode()  # Receive file over socket.
filename, filesize = received.split(SEPARATOR)  # Split out filename and filesize.
filename = os.path.basename(filename)  # Pass our filename and path to the writer.
filesize = int(filesize)  # Pass our filesize to the writer.

# Fancy progress bar.
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
# Write out file received in bytes updating progress bar.
# As well as closing both client and server sockets.
with open(filename, "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
client_socket.close()
s.close()