import socket
import threading
import signal
import sys

HOST = "0.0.0.0"
PORT = 5000

clients = []
usernames = {}  # client_socket -> username

# ANSI color codes
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                pass

def handle_client(client_socket, addr):
    try:
        # Ask for username
        client_socket.send("Enter your username: ".encode("utf-8"))
        username = client_socket.recv(1024).decode("utf-8").strip()
        usernames[client_socket] = username
        clients.append(client_socket)

        broadcast(f"{CYAN}[SERVER]{RESET} {username} has joined the chat!", client_socket)
        print(f"{username} ({addr}) connected.")

        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            broadcast(f"{GREEN}[{username}]{RESET} {message}", client_socket)
    except:
        pass
    finally:
        if client_socket in clients:
            broadcast(f"{CYAN}[SERVER]{RESET} {usernames[client_socket]} has left the chat.", client_socket)
            clients.remove(client_socket)
            del usernames[client_socket]
            client_socket.close()

# Create server socket with reuse option
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"[LISTENING] Server is listening on port {PORT}")

# Handle Ctrl+C (SIGINT) to close server gracefully
def shutdown_server(signal_received, frame):
    print("\n[SHUTDOWN] Closing server...")
    for client in clients:
        client.close()
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_server)

# Main loop
while True:
    try:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
    except Exception as e:
        print(f"[ERROR] {e}")
