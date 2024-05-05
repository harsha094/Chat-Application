import socket
import threading
import hashlib
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
                remove_client(client_socket)
                break
            if msg.startswith('@'):
                recipient_username, private_msg = msg.split(':',1)
                send_private_msg(private_msg, client_socket, recipient_username[1:])
            else:
                print(f"Received message from {address} : {msg}")
                broadcast(msg, client_socket)
        except Exception as e:
            print(f"Error handling client {address}: {e}")
            break

def broadcast(msg, sender_socket):
    username = get_username(sender_socket)
    encrypted_msg = encrypt_msg(msg)
    for client in clients:
        if client != sender_socket:
            try:
                client.send(f"{username}:{encrypted_msg}".encode())
            except Exception as e:
                print(f"Error broadcasting message to a client: {e}")

def send_private_msg(msg, sender_socket, recipient_username):
    sender_username = get_username(sender_socket)
    encrypted_msg = encrypt_msg(msg)
    recipient_socket = get_socket_by_username(recipient_username)
    if recipient_socket:
        try:
            recipient_socket.send(f"{sender_username} (private) : {encrypted_msg}".encode())
        except Exception as e:
            print(f"Error sending private msg to {recipient_username}:{e}")

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        username = get_username(client_socket)
        print(f"{username} has left chat.")
        broadcast(f"{username} has left chat.", client_socket)

def get_username(client_socket):
    return [username for username, socket in clients if socket == client_socket][0]

def get_socket_by_username(username):
    for u, s in clients:
        if u == username:
            return s
    return None

def encrypt_msg(msg):
    return hashlib.sha256(msg.encode()).hexdigest()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9999))
    server_socket.listen(5)
    print("Server Started, listening on port 9999....")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")
        client_socket.send("Enter your Username :".encode())
        username = client_socket.recv(1024).decode()
        clients.append((username, client_socket))
        client_handler = threading.Thread(target = handle_client, args = (client_socket, address))
        client_handler.start()

clients = []

if __name__ == "__main__":
    start_server()