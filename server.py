import socket
import threading
# old simple code code 
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server.bind(("localhost", 9999))

# server.listen()

# client, addr = server.accept()

# done = False

# while not done:
#     msg = client.recv(1024).decode()
#     if msg == 'quit':
#         done = True
#     else:
#         print(msg)
#     client.send(input("Message: ").encode())
# old code ends.

def handle_client(client_socket, address):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                print(f"Connection with {address} closed.")
                break
            print(f"Received message from {address} : {msg}")
            broadcast(msg, client_socket)
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

def broadcast(msg, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(msg.encode())
            except Exception as e:
                print(f"Error broadcasting message to a client: {e}")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("Server Started, listening on port 9999....")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")
        clients.append(client_socket)
        client_handler = threading.Thread(target = handle_client, args = (client_socket, address))
        client_handler.start()

clients = []

if __name__ == "__main__":
    start_server()