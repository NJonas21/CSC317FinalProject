import threading
import socket
import time
import server

class MultiChat(server.MessagingServer):

    def __init__(self):
        self.name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.name)

        self.port = 50001

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.ip_address, self.port))

        self.rooms = {}


    def createServer(self, name):
        self.rooms[name] = MessagingServer()


    def handle_connection(self, client_conn, client_addr):
        choice = self.socket.recv(5).decode("utf-8")

        if choice == "create":
            print("create")
            name = str(self.socket.recv(10)) # Limit group name sizes on client?
            createServer(self, name)
            print(f"{name}, {self.room[name]}")
            tempServer = str(self.room[name])
            tempServerSize = len(tempServer.encode("utf-8"))
            self.socket.send(str(tempServerSize).encode("utf-8"))
            time.sleep(1)
            self.socket.send(tempServer)

            client_conn.close() # Close off the client from this server
            # Client should then use server information to connect to other connection

        elif choice == "join":
            print("join")
            if len(self.rooms) == 0:
                createServer(self, "default")
                print(f"default, {self.room['default']}")
                tempServer = str(self.room["default"])
                tempServerSize = len(tempServer.encode("utf-8"))
                self.socket.send(str(tempServerSize).encode("utf-8"))
                time.sleep(1)
                self.socket.send(tempServer)

                client_conn.close() # Close off the client from this server
                # Client should then use server information to connect to default connection
            else:
                print("Too bad")
                # Add listing function later


    def startChats(self):

        working = True
        self.socket.listen(5)
        while working:
            client_conn, client_addr = self.socket.accept()
            thread = threading.Thread(target=handle_connection, args = (client_conn, client_addr))
            thread.start()
            print(f"Active clients: {threading.activeCount() - 1}")


def main():
    print("Hello World!")

    multiChatSocket = MultiChat()

    multiChatSocket.startChats()


if __name__ == "__main__":
    main()
