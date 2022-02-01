import socket
import tqdm
import os


class XferClient():
    '''Simple file transfer over a socket client. Expects host as str IPadd "127.0.0.1",  port 5001 as int, buffer_size 4096 as int, and separator as str "<SEPARATOR>" '''
    def __init__(self, host, port, buffer_size, separator):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.separator = separator
        
        # TODO: Error handling with some try excepts.
        # TODO: Handle graceful termination w/ keyboard inturupts.
        # TODO: Compress file before sending.
        # TODO: Encrypt file before sending.
        # TODO: Hashing an checksums of the files client and server.
        s = socket.socket()
        print(f"[+] Connecting to {self.host}:{self.port}")
        s.connect((self.host, self.port))  # Make socket conn to host:port.
        print("[+] Connected to ", host)
        filename = input("File to Transfer : ")  # Add full path of file to send.
        # TODO: Handle for windows paths. Or set to a static path.
        filesize = os.path.getsize(filename)  # Get size of file in bytes.
        s.send(f"{filename}{self.separator}{filesize}".encode()) # Send file over socket.

        # Fancy progess bar.
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        # Read our file into the socket as bytes and update progess bar.
        # As well as closing the client socket.
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(self.buffer_size)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
        s.close()
        
        
if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5001
    buffer_size = 4096
    separator = "<SEPARATOR>"
    XferClient(host, port, buffer_size, separator)