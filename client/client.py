import socket
import os
import argparse
import threading # we will create 2 threads: Receivinf msgs and Send msgs.



class Client():
    def __init__(self,host,port,name):
        super().__init__()
        self.host=host
        self.port=port
        self.name=name
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #to communicate with other devices
    
    def start(self):
        print("[*] Connecting to server: " +str(self.host) + "," + str(self.port))
        
        try:
            self.sock.connect((self.host, self.port))
            print("[+] Successfuly connected to server: " +str(self.host) + "," + str(self.port))
        except Exception as e :
            print("[-] Failed to connect to server " +str(self.host) + "," + str(self.port))
            exit(1)
        #send the name of the client
        self.sock.sendall(self.name.encode('ascii'))
        #create send and receive
        send=Send(args.host,args.p,self.sock)
        receive=Receive(args.host,args.p,self.sock)

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
            message= input("Message to send to server: ")
            self.sock.sendall(message.encode('ascii'))


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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    # Create and start client
    client=Client(args.host,args.p,"Lucy")
    client.start()


