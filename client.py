import socket
import threading
import hashlib
import tkinter as tk
from tkinter import messagebox

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

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")
        self.master.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.chat_history = tk.Text(self.master, state='disabled')
        self.chat_history.pack(fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(self.master)
        self.msg_entry.pack(fill=tk.X, side=tk.LEFT, padx=5, pady=5, expand=True)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_msg)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)


    def receive_msg(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                self.display_msg(msg)
            except Exception as e:
                print(f"Error receiving message from server: {e}")
                break
    
    def display_msg(self, msg):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, msg + '\n')
        self.chat_history.configure(state='disabled')

    def send_msg(self):
        msg = self.msg_entry.get()
        if msg:
            try:
                if msg.startswith('@'):
                    recipient_username, private_msg = msg.split(':', 1)
                    self.client_socket.send(msg.encode())
                    self.display_msg(f"You (private to {recipient_username}): {private_msg}")
                else:
                    self.client_socket.send(msg.encode())
                    self.display_msg(f"You : {msg}")
            except Exception as e:
                print(f"Error sending message to server: {e}")
        self.msg_entry.delete(0, tk.END)

    def connect_to_server(self):    
        try:    
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 9999))
            self.display_msg("Connected to server, Enter your Username!")
            self.username = input("Please Enter your Username: ")
            self.client_socket.send(self.username.encode())
            self.receive_thread = threading.Thread(target=self.receive_msg)
            self.receive_thread.start()
            self.msg_entry.bind("<Return>", lambda event: self.send_msg())
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.master.destroy()
            messagebox.showerror("Error", "Failed to connect to server.")

def main():
    root = tk.Tk()
    app = ChatApp(root)
    app.connect_to_server()
    root.mainloop()

if __name__ == "__main__":
    main()