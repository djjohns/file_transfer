import socket
import tqdm
import os


class XferServer():
    '''Spins up a simple socket server to transfer files.
    Expects host as "0.0.0.0", port 5001 as int, buffer_size 4096 as int, and separator as "<SEPARATOR>" '''
    def __init__(self, host, port, buffer_size, separator,):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.separator = separator

        # TODO: Error handling with some try excepts.
        # TODO: Handle graceful termination w/ keyboard inturupts.
        # TODO: Uncompress file before sending.
        # TODO: Dencrypt file before sending.
        # TODO: Hashing an checksums of the files client and server.
        s = socket.socket()  # Create our socket.
        s.bind((self.host, self.port))  # Bind it to our host:port.
        s.listen(10)  # Listen for a connection.
        print(f"[*] Listening as {self.host}:{self.port}")
        print("Waiting for the client to connect... ")
        client_socket, address = s.accept()  # Accept the connection.
        print(f"[+] {address} is connected.")
        received = client_socket.recv(self.buffer_size).decode()  # Receive file over socket.
        filename, filesize = received.split(self.separator)  # Split out filename and filesize.
        # TODO: Set an explict path to write file to.
        filename = os.path.basename(filename)  # Pass our filename and path to the writer.
        filesize = int(filesize)  # Pass our filesize to the writer.

        # Fancy progress bar.
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        # Write out file received in bytes updating progress bar.
        # As well as closing both client and server sockets.
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(self.buffer_size)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
        client_socket.close()
        s.close()
        


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5001
    buffer_size =4096
    separator = "<SEPARATOR>"
    XferServer(host, port, buffer_size, separator)