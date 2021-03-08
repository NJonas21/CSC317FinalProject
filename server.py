
import socket
import threading
import time

class MessagingServer:
    def __init__(self): # Initialize the server
        self.name = socket.gethostname()
        self.disconnect_message = '!disconnect'

        self.ip_address = socket.gethostbyname(self.name)
        self.port = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))

        self.port = self.socket.getsockname()[1]

        self.client_address_info = {} # key: username, value: address
        self.client_socket_info = {}  # key: username, value: socket

        self.unsent_message = [] # key: (sender, message, receiver)

    def print_online_user(self):
        info = [str(u) + ' is online.\n' for u in self.client_address_info.keys()]

        sentences = ''
        for s in info:
            sentences += s

        return sentences

    def receive_message(self, client_conn, client_addr):

        print('\n', f"[NEW CONNECTION] {client_addr} connected.")
        connected = True

        while connected:

            packet = client_conn.recv(1024)

            data = packet.decode('utf-8').split(':')
            client_name, message, forward_user = data[0], data[1], data[2]

            print(data)
            if message == 'Login':
                self.client_address_info[client_name] = client_addr
                self.client_socket_info[client_name] = client_conn

                print('Login!!!')
                client_conn.send(self.print_online_user().encode('utf-8'))
                continue
            elif message == self.disconnect_message:
                break

            print(client_name, ':', message, 'to', forward_user)
            self.unsent_message.append((client_name, message, forward_user))

        client_conn.close()
        self.client_socket_info.pop(client_name, None)

        print(f"[DISCONNECTION] {client_addr} disconnected.")

    def send_message(self):

        print("\n [SENDING_MESSAGE] works. \n")
        # Check if socket still connected #
        while True:

            for packet in self.unsent_message:
                print(f"[CHECKING] {packet}")
                try:
                    sender, message, receivers = packet[0], packet[1], packet[2]

                    entire_message = sender + ':' + message

                     #conn = self.client_socket_info[receivers]
                     #print(entire_message)
                     #conn.send(entire_message.encode('utf-8'))

                    # for multiple forward users
                    for i in receivers.split(','):
                        conn = self.client_socket_info[i]
                        conn.send(entire_message.encode('utf-8'))

                    self.unsent_message.remove(packet)

                    print("Sending succesful!")
                except:
                    pass
            time.sleep(3)

    def run(self):
        self.socket.listen(5)
        print(f"[LISTENING] Server is listening on {self.ip_address}")

        thread_send = threading.Thread(target=self.send_message)
        thread_send.start()

        while True:

            client_conn, client_addr = self.socket.accept()

            #start_new_thread(self.handle_client, (client_conn, client_addr))
            #threading.Thread(target=self.handle_client, args = (client_conn, client_addr)).start()

            thread_receive = threading.Thread(target=self.receive_message, args = (client_conn, client_addr))
            thread_receive.start()

            #thread.join()  join makes second thread unable.
        self.socket.close()


if __name__ == '__main__':
    server = MessagingServer()

    print(server.ip_address)
    print(server.port, '\n')

    print("[STARTING] server is starting...")
    server.run()
