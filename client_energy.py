import socket
import threading
import psutil
import time

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345


def log_resource_usage():
    """Continuously logs CPU and memory usage."""
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory().percent
        print(f"[CLIENT RESOURCE USAGE] CPU: {cpu_usage}%, Memory: {memory_info}%")
        time.sleep(1)


def receive_messages(client_socket):
    """Receive messages from the server and display them."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except ConnectionResetError:
            print("Disconnected from the server.")
            break


def start_client():
    """Connect to the server and handle message exchange."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the server.")

    # Start resource monitoring in a separate thread
    resource_monitor_thread = threading.Thread(target=log_resource_usage)
    resource_monitor_thread.daemon = True
    resource_monitor_thread.start()

    # Start a thread to listen for incoming messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        client_socket.sendall(message.encode())
        if message.lower() == 'bye':
            print("Disconnecting from the server.")
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()
