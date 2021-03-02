import socket
import threading

class MessagingServer:
    def __init__(self): # Initialize the server
        self.name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.name)

        self.port = 50001

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.ip_address, self.port))


    def startUp(self):
        self.socket.listen(5)
        while True:
            client_conn, client_addr = self.socket.accept()
            thread = threading.Thread(target=handle_client, args = (client_conn, client_addr))
            thread.start()
            print(f"Active clients: {threading.activeCount() - 1}")



def main(): #Delete later
    print("Hello World!")

    serverSocket = MessagingServer()

    print(serverSocket.ip_address)

    print(serverSocket.port)





if __name__ == "__main__": # Also Delete later
    main()
