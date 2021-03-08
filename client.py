import socket
import time
import threading

class MessagingClient:
    def __init__(self, username): #Initializes Client
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = 10001

        self.name = username
        self.client_addr = (self.ip_address, self.port)

    def connect(self, server_ip, server_port):
        self.server_addr = (server_ip, server_port)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_addr)

        connectBool = True
        while connectBool:
            choice = input("Would you like to join or create a chat?")


            if choice == "join":
                self.client_socket.send(choice.encode("utf-8"))

                listSize = int(self.client_socket.recv(5).decode("utf-8"))

                chatList = self.client_socket.recv(listSize).decode("utf-8")
                if len(chatList) == 0:
                    print("receiving default server...")
                    connectBool = False
                else:
                    chatList.split(",")
                    print(chatList)
                    while True:
                        chatChoice = input("Choose a server from the list: ")
                        if chatChoice in chatList:
                            self.client_socket.send(chatChoice.encode("utf-8"))
                            break
                        else:
                            print("Choose a valid name.")
                connectBool = False
            elif choice == "create":
                self.client_socket.send(choice.encode("utf-8"))

                listSize = int(self.client_socket.recv(5).decode("utf-8"))

                chatList = self.client_socket.recv(listSize).decode("utf-8")
                chatList.split(",")
                print(chatList)
                while True:
                    chatChoice = input("Choose a name for your server that isn't already taken: ")
                    if chatChoice not in chatList:
                        self.client_socket.send(chatChoice.encode("utf-8"))
                        break
                    else:
                        print("choose a valid name.")
                connectBool = False
            else:
                print("Not a valid option, please choose either 'create' or 'join'")
        print("While loop passed")
        chat_addr_size = int(self.client_socket.recv(5).decode("utf-8"))

        print("size received")

        chat_addr = self.client_socket.recv(chat_addr_size).decode("utf-8")

        self.disconnect()

        print("disconnected")

        print(chat_addr)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chat_addr_split = chat_addr.split(",")

        self.client_socket.connect((chat_addr_split[0], int(chat_addr_split[1])))

        self.login()
        print("[Login] Login succeedes.\n")

    def login(self):
        print("Logging in")
        packet = self.name + ':' + 'Login' + ':' + ''
        encoded_packet = packet.encode("utf-8")

        self.client_socket.send(encoded_packet)

    def message(self, message='', user=''):

        while True:
            message = input('Type messaging text and forward user here....(e.g. text->name)\n').split('->')
            packet = self.name + ':' + message[0] + ':' + message[1].strip()
            encoded_packet = packet.encode("utf-8")

            self.client_socket.send(encoded_packet)

    def receive(self):

        while True:
            response = self.client_socket.recv(1024)

            if response:
                print(response.decode("utf-8"))

    def disconnect(self):
        self.client_socket.close()

    def run(self, server_ip, server_port):
        self.connect(server_ip, server_port)

        threading.Thread(target=self.receive).start()
        self.message()

def main():
    username = input("Please input username: ")

    client = MessagingClient(username)
    client.run("10.104.65.5", 50001)



if __name__ == "__main__":
    main()
