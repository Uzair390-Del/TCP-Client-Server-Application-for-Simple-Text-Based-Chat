import socket

# Server configuration
SERVER_IP = "127.0.0.1"  # Localhost for testing
SERVER_PORT = 12345

def start_server():
    """Starts the TCP server and handles client communication."""
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the IP and port
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server started at {SERVER_IP}:{SERVER_PORT}")

    # Listen for incoming connections (1 client for simplicity)
    server_socket.listen(1)
    print("Waiting for a client to connect...")

    # Accept client connection
    client_socket, client_address = server_socket.accept()
    print(f"Client connected from {client_address}")

    # Handle communication with the client
    while True:
        # Receive data from the client
        message = client_socket.recv(1024).decode()
        if message.lower() == 'bye':
            print("Client has disconnected.")
            break

        print(f"Client: {message}")
        
        # Send a response
        server_response = input("Server: ")
        client_socket.sendall(server_response.encode())

    # Close the sockets
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
