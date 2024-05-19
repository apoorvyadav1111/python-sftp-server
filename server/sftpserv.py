import ssl, socket
import sys
import fs
# https://docs.python.org/3/library/ssl.html#server-side-operation

class SSLServerWrapper:
    def __init__(self, cert, key, port):
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert, keyfile=key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("",port))
        self.socket.listen(5)
    
    def listen_to_client(self):
        while True:
            new_socket, fromaddr = self.socket.accept()
            connstream = self.context.wrap_socket(new_socket, server_side=True)
            while True:
                data = connstream.recv(1024).decode()
                data = data.split('$#')
                if len(data)>1:
                    cmd, file = data
                    if cmd == 'get':
                        try:
                            s = 0
                            with open(file,'rb') as f:
                                connstream.send('FILE_FOUND'.encode())
                                line = f.read(1024)
                                s += len(line.decode())
                                while line:
                                    connstream.send(line)
                                    line = f.read(1024)
                            print(f'{s} characters transferred for file {file}')
                            connstream.send('FILE_SEND_COMPLETE'.encode())
                        except:
                            connstream.send('FILE_NOT_FOUND'.encode())

                else:
                    cmd = data[0]
                    if cmd == 'hello':
                        continue
                    elif cmd == 'exit':
                        connstream.close()
                        sys.exit()
                    else:
                        connstream.send('INVALID_COMMAND'.encode())
            connstream.close()
                    
        

def main():
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
            if not 1024<=port<=65535:
                print("Port value should be between 1024 and 65535")
                sys.exit()
        except Exception as e:
            print("Please check the value of the port")
            sys.exit()
    else:
        port = 7654 
    sslwrapper = SSLServerWrapper("cert.pem", "key.pem", port)
    try:
        sslwrapper.listen_to_client()
    finally:
        sslwrapper.socket.close()


if __name__ == "__main__":
    main()