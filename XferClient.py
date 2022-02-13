import socket
import tqdm
import os


class XferClient():
    '''
    ### Simple file transfer client over a socket.
    #### Args
    host (str): IP address of the server or FQDN. In development use "127.0.0.1".
    
    port (int): This is the port number that is open on the server. In our case for development it is port 5001.
    
    buffer_size (int): The reserved segment of memory allocated for transfer progress. This value should be the same on both server and client. Currently this is set to 4096.
    
    separator (str): This is what indicates the seperation between the information we send over the socket to the server. Currently this is set to "<SEPARATOR>".
    #### Implementation example
    ```
    from file_transfer import XferClient
    
    host = "127.0.0.1"
    port = 5001
    buffer_size = 4096
    separator = "<SEPARATOR>"
    XferClient(host, port, buffer_size, separator)
    ``` 
    '''
    def __init__(self, host, port, buffer_size, separator):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.separator = separator
        # TODO: Handle graceful termination w/ keyboard inturupts.
        # TODO: Compress file before sending.
        # TODO: Encrypt file before sending.
        # TODO: Hashing an checksums of the files client and server.
        try:
            # Filepath to the dir we place all of our files to transfer.
            src_dir = os.path.realpath('C:/dev/FilesToTransfer')
            try:
                for filename in os.listdir(src_dir):
                    s = socket.socket()
                    print(f"[+] Attpeting connection to: {self.host}:{self.port}")
                    s.connect((self.host, self.port))  # Make socket conn to host:port.
                    print(f"[+] Connection established to: {self.host}:{self.port}")
                    filesize = os.path.getsize(os.path.join(src_dir,filename))  # Get size of file in bytes
                    s.send(f"{filename}{self.separator}{filesize}".encode()) # Send file, separator,and filesize over socket.
                    # Read our file into the socket as bytes and update progess bar.
                    progress = tqdm.tqdm(range(filesize), f"[+] Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                    with open(os.path.join(src_dir,filename), "rb") as fh:
                        while True:
                            bytes_read = fh.read(self.buffer_size)
                            if not bytes_read:
                                break
                            s.sendall(bytes_read)
                            progress.update(len(bytes_read))
                s.close()  # Remember to close the socket.
            except Exception as e:
                s.close()  # Close the socket if we throw an exception.
                print(e)
            s.close()  # Remember to close the socket.
        except Exception as e:
            print(e)




if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5001
    buffer_size = 4096
    separator = "<SEPARATOR>"
    XferClient(host, port, buffer_size, separator)