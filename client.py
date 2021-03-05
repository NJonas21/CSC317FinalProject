import socket
import time

class MessagingClient:
    def __init__(self): #Initializes Client
        self.name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.name)

        self.server_port = 50001

        self.port = 0

        self.client_addr = (self.ip_address, self.port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.client_socket)

    def connect(self, server_ip):
        self.server_addr = (server_ip, self.server_port)

        self.client_socket.connect(self.server_addr)

    def message(self, message):
        encodeMsg = message.encode("utf-8")
        '''
        bufsize = len(encodeMsg)

        self.client_socket.send(str(bufsize).encode("utf-8"))

        time.sleep(1)

        conf = self.client_socket.recv(8)
        '''
        self.client_socket.send(encodeMsg)

    def receive(self):
        responseSize = self.client_socket.recv(4).decode("utf-8")
        responseSizeStr = str(responseSize)
        responseSizeInt = int(responseSizeStr)
        response = self.client_socket.recv(responseSizeInt).decode("utf-8")

        print(response) #For Testing
        return response

    def diconnect(self):
        self.client_socket.close()

def main():

    clientSocket = MessagingClient()
    clientSocket.connect("10.104.65.5")
    clientSocket.message("join")

    control = True
    while control:
        time.sleep(1)
        response = clientSocket.receive()
        if response == "%end":
            control = False

    clientSocket.close()

if __name__ == "__main__":
    main()
