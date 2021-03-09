# Authors: Nick Jonas, Bram Dedrick, Chenxi Liu
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

        self.working = True

        self.rooms = {}

    def create_server(self, name):
        self.rooms[name] = server.MessagingServer()

    def heart_beat(self):
        for k in self.rooms.keys():
            if self.rooms[k].client_count == 0:
                self.rooms[k].is_working = False

        self.rooms = {k: v for (k, v) in self.rooms.items() if self.rooms[k].client_count != 0}

    def handle_connection(self, client_conn):
        if len(self.rooms) > 0:
            self.heartBeat()
        choice = client_conn.recv(6).decode("utf-8")
        keys = ",".join(self.rooms.keys())
        keys_enc = keys.encode("utf-8")
        keys_length = len(keys_enc)
        client_conn.send(str(keys_length).encode("utf-8"))
        client_conn.send(keys_enc)
        if choice == "create":
            while self.working:
                name = str(client_conn.recv(15).decode("utf-8"))  # Limit group name sizes on client?
                if name not in self.rooms.keys():
                    self.createServer(name)
                    temp_server = f"{self.rooms[name].ip_address},{self.rooms[name].port}".encode("utf-8")
                    temp_server_size = len(temp_server)
                    client_conn.send(str(temp_server_size).encode("utf-8"))
                    time.sleep(1)
                    client_conn.send(temp_server)

                    client_conn.close()  # Close off the client from this server
                    # Client should then use server information to connect to other connection
                    self.rooms[name].run()
                    break

        elif choice == "join":
            if len(self.rooms) == 0:
                self.createServer("default")
                temp_server = f"{self.rooms['default'].ip_address},{self.rooms['default'].port}"
                temp_server_size = len(temp_server.encode("utf-8"))
                client_conn.send(str(temp_server_size).encode("utf-8"))
                time.sleep(1)
                client_conn.send(temp_server.encode("utf-8"))

                client_conn.close()  # Close off the client from this server
                # Client should then use server information to connect to default connection
                self.rooms["default"].run()

            else:  # There are chat rooms available
                max_str = -1
                for i in self.rooms.keys():  # Grab the max string size used in the room names
                    if max_str < len(i):
                        max_str = len(i)
                name = client_conn.recv(max_str).decode("utf-8")  # Receive choice
                time.sleep(1)
                temp_server = f"{self.rooms[name].ip_address},{self.rooms[name].port}"  # Find the server of choice
                temp_server_enc = temp_server.encode("utf-8")
                temp_server_size = len(temp_server_enc)
                client_conn.send(str(temp_server_size).encode("utf-8"))  # Send the sever information length
                time.sleep(1)
                client_conn.send(temp_server_enc)  # Send Server information

                client_conn.close()  # Close the connection

                self.rooms[name].run()

    def command_line(self):
        while self.working:
            command = input("\n")
            if command == "!quit":
                self.disconnect()
                self.working = False
                for k in self.rooms.keys():
                    self.rooms[k].socket.close()
                    self.rooms[k].is_working = False
                print("Closed")
            else:
                print("Invalid command")

    def start_chats(self):
        self.socket.listen()
        while self.working:
            try:
                client_conn, client_addr = self.socket.accept()
                client_conn.close()
                client_conn, client_addr = self.socket.accept()
                print(self.rooms)
                thread = threading.Thread(target=self.handle_connection, args=(client_conn, client_addr))
                thread.start()
            except:
                break

    def disconnect(self):
        self.socket.close()


def main():
    multi_chat_socket = MultiChat()

    print(multi_chat_socket.ip_address)
    print(multi_chat_socket.port)
    thread_command_line = threading.Thread(target=multi_chat_socket.command_line)
    thread_command_line.start()
    thread = threading.Thread(target=multi_chat_socket.start_chats)
    thread.start()


if __name__ == "__main__":
    main()
