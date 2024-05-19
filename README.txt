### Details

### References:
The code for ssl connection is found from python documentation website here:

```
https://docs.python.org/3/library/ssl.html#server-side-operation
```

### Testing on Remote CS
The code was written and thoroughly tested on remote cs machine

### Running the program
Please **untar** the submission and cd into the directory.
The code running setup is minimal. The server code is in **server** directory which contains keys and certificate. 
The client code is in **client** folder. 
The file **sftpcli.py** needs the file **cert.perm** hence the relative path for server and client must be kept same. 
The server folder also contains a sample file **a.txt** to test the program.


1. Start the server (default port is 7654). Please enter the PEM pass phrase: .
```
cd server
python3 server.py 
```
**or**
```
cd server
python3 server.py <port>
```

2. Start the client, (please change the port and host as needed)
```
cd client
python3 sftpcli.py <host> 7654
```

### Description
The program works in the following steps:
1. Client program checks for the command, if invalid: show error and prompt for new input
2. If it is a get command, the client checks for a filename. It should not be empty
3. Client sends the command to server, which checks for the file. If found, server sends back 'FILE_FOUND' else 'FILE_NOT_FOUND'.
4. If FILE_FOUND

    a. then client creates an empty file and recieve the data until server sends 'FILE_SEND_COMPLETE' complete.
    
    b. server prints the number of characters sent.

    c. client prints the number of characters recieved and the time.

5. else, client prompts error message and prompts for user input again.
6. If command is exit, client sends exit to the server and both program exits.

### Credits
https://docs.python.org/3/library/ssl.html#server-side-operation