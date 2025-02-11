import socket
import threading
import psutil
import time

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
clients = []


def log_resource_usage():
    """Continuously logs CPU and memory usage."""
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory().percent
        print(f"[SERVER RESOURCE USAGE] CPU: {cpu_usage}%, Memory: {memory_info}%")
        time.sleep(1)  # Adjust the interval as necessary


def handle_client(client_socket, client_address):
    """Handle communication with a single client."""
    print(f"Client {client_address} connected.")
    clients.append(client_socket)

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode()
            if not message or message.lower() == 'bye':
                print(f"Client {client_address} disconnected.")
                break

            print(f"{client_address}: {message}")
            broadcast_message(f"{client_address}: {message}", client_socket)

        except ConnectionResetError:
            print(f"Client {client_address} disconnected unexpectedly.")
            break

    clients.remove(client_socket)
    client_socket.close()


def broadcast_message(message, sender_socket):
    """Send the message to all connected clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except Exception:
                continue


def start_server():
    """Start the server and accept multiple client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started at {SERVER_IP}:{SERVER_PORT}. Waiting for connections...")

    # Start resource monitoring in a separate thread
    resource_monitor_thread = threading.Thread(
        target=log_resource_usage)
    resource_monitor_thread.daemon = True
    resource_monitor_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    start_server()
