import socket
import threading

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345


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
    """Connect to the server and handle sending and receiving messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the server.")

    # Start a thread to listen for incoming messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Send message to the server
        message = input()
        client_socket.sendall(message.encode())

        if message.lower() == 'bye':
            print("Disconnecting from the server.")
            break

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    start_client()
