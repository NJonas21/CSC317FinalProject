# Authors: Nick Jonas, Bram Dedrick, Chenxi Liu
import socket
import threading
import time


class MessagingServer:
    def __init__(self):  # Initialize the server
        self.name = socket.gethostname()
        self.disconnect_message = '!disconnect'

        self.ip_address = socket.gethostbyname(self.name)
        self.port = 0

        self.client_count = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))

        self.port = self.socket.getsockname()[1]

        self.client_address_info = {}  # key: username, value: address
        self.client_socket_info = {}  # key: username, value: socket

        self.unsent_message = []  # key: (sender, message, receiver)

        self.is_working = True

    def print_online_user(self):
        info = [str(u) + ' is online.\n' for u in self.client_address_info.keys()]

        sentences = ''
        for s in info:
            sentences += s

        return sentences

    def receive_message(self, client_conn, client_addr):
        self.client_count += 1

        while self.is_working:

            packet = client_conn.recv(1024)

            data = packet.decode('utf-8').split(':')
            client_name, message, forward_user = data[0], data[1], data[2]

            if message == 'Login':
                self.client_address_info[client_name] = client_addr
                self.client_socket_info[client_name] = client_conn

                client_conn.send(self.print_online_user().encode('utf-8'))
                continue
            elif message == self.disconnect_message:
                self.client_count = self.client_count - 1
                break
            elif message != self.disconnect_message and forward_user == "":
                forward_user = ",".join(self.client_socket_info.keys())

            self.unsent_message.append((client_name, message, forward_user))

        client_conn.close()
        self.client_socket_info.pop(client_name, None)


        if self.client_count == 0:
            self.socket.close()

    def send_message(self):
        # Check if socket still connected #
        while self.is_working:

            for packet in self.unsent_message:
                try:
                    sender, message, receivers = packet[0], packet[1], packet[2]

                    entire_message = sender + ':' + message

                    # for multiple forward users
                    for i in receivers.split(','):
                        conn = self.client_socket_info[i]
                        conn.send(entire_message.encode('utf-8'))

                    self.unsent_message.remove(packet)
                except:
                    pass
            time.sleep(3)

    def run(self):
        self.socket.listen()

        thread_send = threading.Thread(target=self.send_message)
        thread_send.start()

        while self.is_working:
            try:
                client_conn, client_addr = self.socket.accept()

                thread_receive = threading.Thread(target=self.receive_message, args=(client_conn, client_addr))
                thread_receive.start()
            except:
                break

        self.socket.close()


if __name__ == '__main__':
    server = MessagingServer()
    server.run()
