import socket
import threading
import os
import platform

SERVER_IP = input("Enter the server IP address: ")
PORT = 5000

message_history = []

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_messages():
    clear_screen()
    for msg in message_history[-10:]:  # Show last 10 messages
        print(msg)

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                message_history.append(message)  # Keep exactly what server sent
                display_messages()
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Receive username prompt and send username
prompt = client_socket.recv(1024).decode("utf-8")
username = input(prompt)
client_socket.send(username.encode("utf-8"))

# Start receiving messages
recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
recv_thread.start()

# Main loop
print("Type messages below. Type '/quit' to exit.")
while True:
    msg = input()
    if msg.lower() == "/quit":
        client_socket.close()
        break
    client_socket.send(msg.encode("utf-8"))
