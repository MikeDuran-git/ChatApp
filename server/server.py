import threading # so that i can create a thread for each user
import socket
import os
import argparse

#Specific server that handles a specific client
class ServerSocket(threading.Thread):

    def __init__(self, client, sockname, server):
        super().__init__()
        self.client = client
        self.sockname = sockname
        self.server = server
        self.client_name= None
    
    def run(self):
        
        self.client_name=self.client.recv(1024).decode('ascii')#get the name
        print(self.client_name + " connected")
        
        while True: #a true loop inside the specific thread for the client.
            message=self.client.recv(1024).decode('ascii')# waiting for client message
            if message:
                print(str(self.client_name) + "  : "+ str(message))
                self.client_message_management(message)            
            else:
                # Client has closed the socket, exit the thread
                print('{} has closed the connection'.format(self.sockname))
                self.client.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        self.client.sendall(message.encode('ascii'))
        pass

    def client_message_management(self,message):
        if message == "private message": #send to a specific client
            
            #sent to the client the list of all clients
            clients_list=self.get_clients_list()
            print("[*] SENDING CLIENT LIST")
            self.send(clients_list)
            
            #wait for the client to choose the target
            target_and_message=self.client.recv(1024).decode('ascii')
            
            #set target and msg
            target=target_and_message.split(':')[0]
            msg=target_and_message.split(':')[1]
            
            #send msg to target
            self.private_send(msg,target)                    

            return
        elif message == "public message": # send to all clients
            #what the client broadcasts to everyone
            message=self.client.recv(1024).decode('ascii')
            print('{} : {!r}'.format(self.client_name, message))
            self.server.broadcast(message, self.sockname)
            return
        elif message=="q" or message=="disconnection":
            self.client_disconnecting()

    def private_send(self,msg,target):
        for connection in self.server.connections:
            if connection.client_name == target:
                print("sending message to " + str(connection.client_name))
                msg=str(self.client_name)+": "+ msg
                connection.send(msg)
                return
        pass

    def get_clients_list(self):
        list=""
        for connection in self.server.connections:
            list = list + str(connection.client_name) +":"+ str(connection.sockname) +"|" 
        return list

    def client_disconnecting(self):
        print("[*] Disconnecting "+str(self.client_name) )
        


#ACTUAL SERVER 
class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        # creation of the socket to communicate with other devices
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SOCK_STREAM because we use TCP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #to bind the socket object to a host and a port on the server machine
        sock.bind((self.host, self.port))

        sock.listen(1) # this is a listening socket. not a connecting one.
        print('Listening at', sock.getsockname())

        while True:
            #Accepting a new connection from a client
            client, client_ip = sock.accept() #waits till client connects
            print("[+] New Client connection from: ",str(client_ip))
            #create a new thread for this client
            server_socket = ServerSocket(client, client_ip, self)
            # Start new thread
            server_socket.start()
        # Add thread to active connections
            self.connections.append(server_socket)
            print('[+] Ready to receive messages from', client.getpeername()) # return client socket adress on the other end of connection.


    def broadcast(self, message, source):
        print("[*] Start of broadcasting message of " +str(source))
        for connection in self.connections:
            # Send to all connected clients except the source client
            if connection.sockname != source:
                connection.send(message)
                print("[+] Sending to " + str(connection.sockname))
    

    def send(self,message,source):
        source=int(source)
        print("[*] Sending message to "+ str(self.connections[source].sockname))
        try:
            self.connections[source].send(message.encode('ascii'))
            print("[+] Message Sended to " + str(self.connections[source].sockname))
        except Exception :
            print("[-] Couldn't send message to: " + str(self.connections[source].sockname))
        pass


# function that is the thread that manages the sending of the server
def server_managing(server):
    while True:
        ipt = input('')
        
        if ipt == 'q':
            print('[*] Closing all connections...')
            for connection in server.connections:
                try:
                    print("[*] Closing " + str(connection.sockname))
                    connection.client.sendall("QUIT".encode('ascii'))
                    connection.client.close()
                    print("[+]" +str(connection.sockname)+" successfuly closed")
                except Exception :
                    print("[-] Closing "+str(connection.sockname)+" failed.")
    
            print('[*] Shutting down the server...')
            os._exit(0)
        
        elif ipt == 'show clients' or ipt=='clients':
            for connection in server.connections:
                print(str(connection.sockname) + " : "+ str(connection.client_name))
        
        elif ipt =="send":
            target=input("Target : ")
            msg=input("Message: ")
            print("sending msg to "+ str(server.connections[int(target)].sockname))
            server.connections[int(target)].send(msg)
            pass

HOST='172.104.145.43'
PORT=1111

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    # Create and start server thread
    server = Server(args.host, args.p)
    server.start()

    server_managing = threading.Thread(target = server_managing, args = (server,))
    server_managing.start()