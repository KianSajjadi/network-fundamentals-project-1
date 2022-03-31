
from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverPort = 8080
server_address = "192.168.0.3" #whatever ip
serverSocket.bind((server_address, serverPort))
serverSocket.listen(1)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print(f"CONNECT TO {addr}")
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]                 
        f = open(filename[1:])                        
        outputdata = f.read()
        #Send one HTTP header line into socket
        connectionSocket.send("""HTTP/1.0 200 OK
          Content-Type: text/html
          &lt;html&gt;
          &lt;head&gt;
          &lt;title&gt;Success&lt;/title&gt;
          &lt;/head&gt;
          &lt;body&gt;
          Your file Exists!
          &lt;/body&gt;
          &lt;/html&gt;
          """.encode())
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        exit()
    except IOError:
        #Send response message for file 
        print ("404 Not Found")
        connectionSocket.send("""HTTP/1.0 404 Not Found\r\n""".encode());
        #Close client socket
        serverSocket.close()
        #Fill in end
        exit()