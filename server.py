import socket
import threading
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
SERVER_NAME = os.getenv('SERVER_NAME')
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS'))
LOG_LEVEL = os.getenv('LOG-LEVEL')
LINUX_PATH = os.getenv('LINUXPATH')
TIMEOUT = int(os.getenv('TIMEOUT'))
DEBUG_MODE = os.getenv('DEBUG_MODE').lower() == 'true'

def handle_client(client_socket, address, file_path):
    """
    Function to handle client connections.
    :param client_socket: The socket object for the client connection.
    :param address: The address of the client.
    :param file_path: The path to the file specified in the configuration.
    """
    print(f"[INFO] Connection established with {address}")
    
    try:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            return
        
        # Decode the received bytes to a string
        search_string = data.decode('utf-8').strip()
        print(f"[INFO] Searching for string: '{search_string}' in the file: {file_path}")
        
        # Open the file and search for a full line match
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() == search_string:
                    # Found a full match
                    client_socket.sendall(b"STRING EXISTS")
                    return
        
        # If no match is found
        client_socket.sendall(b"STRING DOES NOT EXIST")
    
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        client_socket.sendall(b"File not found on the server.")
    
    except ConnectionResetError:
        print(f"[WARNING] Connection lost with {address}")
    
    finally:
        # Close the connection
        client_socket.close()
        print(f"[INFO] Connection closed with {address}")

def start_server():
    """
    Starts the server and listens for incoming connections.
    """
    file_path = LINUX_PATH
    
    if not file_path:
        print("[ERROR] 'LINUXPATH' not found in the environment file.")
        return
    
    print(f"[INFO] File path from environment: {file_path}")
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow address reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    
    # Set the maximum number of connections
    server_socket.listen(MAX_CONNECTIONS)
    print(f"[INFO] Server '{SERVER_NAME}' listening on {HOST}:{PORT} with max connections: {MAX_CONNECTIONS}")
    
    while True:
        # Accept incoming connections
        client_socket, address = server_socket.accept()
        
        # Set the timeout for the client connection
        client_socket.settimeout(TIMEOUT)
        
        # Create a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, file_path))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()
