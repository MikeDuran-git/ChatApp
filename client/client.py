import socket
import os
import argparse
import threading # we will create 2 threads: Receivinf msgs and Send msgs.



class Client():
    def __init__(self,host,port):
        super().__init__()
        self.host=host
        self.port=port
        self.name=None
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #to communicate with other devices
    
    def start(self):
        print("[*] Connecting to server: " +str(self.host) + "," + str(self.port))
        
        try:
            self.sock.connect((self.host, self.port))
            print("[+] Successfuly connected to server: " +str(self.host) + "," + str(self.port))
        except Exception :
            print("[-] Failed to connect to server " +str(self.host) + "," + str(self.port))
            exit(1)
        
        #send the name of the client
        self.name=input("Whats your name ? : ")
        self.sock.sendall(self.name.encode('ascii'))
        
        #create send and receive
        send=Send(self.host,self.port,self.sock)
        receive=Receive(self.host,self.port,self.sock)

        #start them
        send.start()
        receive.start()


class Send(threading.Thread):
    def __init__(self,host,port,personal_socket):
        super().__init__()
        self.host = host
        self.port = port
        self.sock=personal_socket
        pass
    
    def run(self):
        while True: 
            request=input("What is your request? : ")
            
            if request=="quit":
                self.sock.close()
                print("disconnecting from server")
                os._exit(0)
            
            self.request_to_server(request)

    def request_to_server(self,request):
        #we send the request to the server, then act accordingly.
        self.sock.sendall(request.encode('ascii'))
        
        #what does the client do ?
        if request == "private message": #send to a specific client
            #show all clients online
            print("[*] List of all connected clients, select one:")
            
            client_list=self.sock.recv(1024).decode('ascii')
            
            self.show_client_list(client_list)
            #select the client to send the message
            target=input("[*] Target: ")
            msg=input("[*] Message: ")

            msg=str(target) + ":" +str(msg)
            self.sock.sendall(msg.encode('ascii'))
            pass

        elif request == "public message": # send to all clients
            message= input("Message to send to server: ")
            self.sock.sendall(message.encode('ascii'))
            print("[*] Message sended to all connected Clients")
            pass
        



    def show_client_list(self,client_list):
        for client_sockname in client_list.split("|"):
            if client_sockname != "":
                if client_sockname.split(":")[0]== self.client_name:
                    print(client_sockname + " (You)")
                else:
                    print(client_sockname)
        pass

class Receive(threading.Thread):
    def __init__(self,host,port,personal_socket):
        super().__init__()
        self.host = host
        self.port = port
        self.sock=personal_socket
        pass
    
    def run(self):
        while True:
            message = self.sock.recv(1024)
            if message:
                print("\n"+message.decode('ascii'))
            else:
                # Server has closed the socket, exit the program
                print('[*] lost connection to the server')
                print('[*] Quitting...')
                self.sock.close()
                os._exit(0)


HOST='172.104.145.43'
PORT=1111

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    # Create and start client
    client=Client(args.host,args.p)
    client.start()


