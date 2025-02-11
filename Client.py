import socket

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345

def start_client():
    """Connects to the server and handles message exchange."""
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the server.")

    while True:
        # Send message to the server
        client_message = input("Client: ")
        client_socket.sendall(client_message.encode())

        if client_message.lower() == 'bye':
            print("Disconnected from the server.")
            break

        # Receive and display the server response
        server_response = client_socket.recv(1024).decode()
        print(f"Server: {server_response}")

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    start_client()
