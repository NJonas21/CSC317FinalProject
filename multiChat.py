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

        print("bound")

        self.rooms = {}


    def createServer(self, name):
        self.rooms[name] = MessagingServer()


    def handle_connection(self, client_conn, client_addr):
        choice = client_conn.recv(5).decode("utf-8")

        if choice == "create":
            print("create")
            while True:
                name = str(self.socket.recv(10)) # Limit group name sizes on client?
                if name not in self.room.keys():
                    createServer(self, name)
                    print(f"{name}, {self.room[name]}")
                    tempServer = str(self.room[name])
                    tempServerSize = len(tempServer.encode("utf-8"))
                    self.socket.send(str(tempServerSize).encode("utf-8"))
                    time.sleep(1)
                    self.socket.send(tempServer)

                    client_conn.close() # Close off the client from this server
                    # Client should then use server information to connect to other connection
                    break

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
            else: # There are chat rooms available
                keys = ",".join(self.rooms.keys())
                keys_enc = keys.encode("utf-8")
                keys_length = len(keys_enc)
                max_str = -1
                for i in self.rooms.keys(): # Grab the max string size used in the room names
                    if max_str < len(i):
                        max_str = len(i)

                self.socket.send(str(keys_length).encode("utf-8"))
                time.sleep(1)
                self.socket.send(keys_enc) # Send the list of rooms
                # Client will then need to chose and send it back
                choice = self.socket.recv(max_str).decode("utf-8") # Receive choice
                time.sleep(1)
                tempServer = str(self.room[choice]) # Find the server of choice
                temp_server_enc = tempServer.encode("utf-8")
                tempServerSize = len(temp_server_enc)
                self.socket.send(str(tempServerSize).encode("utf-8")) # Send the sever information length
                time.sleep(1)
                self.socket.send(temp_server_enc) # Send Server information

                client_conn.close()# Close the connection


    def startChats(self):

        working = True
        self.socket.listen(5)
        while working:
            client_conn, client_addr = self.socket.accept()
            print("Accepted")
            print(f"{client_conn}, {client_addr}")
            thread = threading.Thread(target=self.handle_connection, args = (client_conn, client_addr))
            thread.start()
            print(f"Active clients: {threading.activeCount() - 1}")


def main():
    print("Hello World!")

    multiChatSocket = MultiChat()

    print(multiChatSocket.ip_address)
    print(multiChatSocket.port)

    multiChatSocket.startChats()


if __name__ == "__main__":
    main()
