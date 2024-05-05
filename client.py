import socket
import threading

#old simple code
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client.connect(("localhost", 9999))

# done = False
# while not done:
#     client.send(input("Message: ").encode())
#     msg = client.recv(1024).decode()
#     if msg == "quit":
#         done = True
#     else:
#         print(msg)
    #old code ends!

def receive_msg():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print("\n" + msg)
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break

def send_msg():
    while True:
        try:
            msg = input()
            client_socket.send(msg.encode())
        except Exception as e:
            print(f"Error sending message to server: {e}")
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9999))

receive_thread = threading.Thread(target=receive_msg)
receive_thread.start()

send_thread = threading.Thread(target=send_msg)
send_thread.start()

