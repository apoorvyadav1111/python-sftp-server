import socket, ssl
import sys
import re
from  datetime import datetime

class SSLClientWrapper:
    def __init__(self, cert, server, port):
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(cert)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.conn = self.context.wrap_socket(self.socket, server_hostname=server)
        self.conn.connect((server, port))

def main():
    if len(sys.argv) < 3:
        print("Require 3 arguments")
        sys.exit()
    else:
        server = sys.argv[1]
        try:
            port = int(sys.argv[2])
            if not 1024<=port<=65535:
                print("Port value should be between 1024 and 65535")
                sys.exit()
        except Exception as e:
            print("Please check the value of the port")
            sys.exit()

    sslclient = SSLClientWrapper("../server/cert.pem", server, port)

    try:
        while True:
            print('sftp >', end='')
            command = input()
            if 'get' in command:
                match = re.match(r"^([^\s]+)\s+(.*?)$", command)
                if match:
                    cmd = match.group(1)
                    file = match.group(2)
                    if file == "":
                        print("Invalid Command: get, needs filename")
                    else:
                        parseCmd = f'{cmd}$#{file}'
                        sslclient.conn.send(parseCmd.encode())
                        line = sslclient.conn.recv(1024)
                        if line == b'FILE_NOT_FOUND':
                            print('sftp >', 'File not found')
                        else:
                            with open(file,'wb') as f:
                                line = sslclient.conn.recv(1024)
                                if line == b'FILE_NOT_FOUND':
                                    print('sftp >', 'File not found')
                                else:
                                    s = 0
                                    while line!=b'FILE_SEND_COMPLETE':
                                        # print('recving', line)
                                        s += len(line.decode())
                                        f.write(line)
                                        line = sslclient.conn.recv(1024)
                                    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} : {s} characters received for file {file}')
                else:
                    print("The file does not exist")
            elif command == 'exit':
                sslclient.conn.send('exit'.encode())
                sslclient.conn.close()
                sslclient.socket.close()
                sys.exit()
            else:
                print("Invalid command")
    finally:
        sslclient.conn.close()
        sslclient.socket.close()

if __name__ == "__main__":
    main()