import socket
import threading
import os
from dotenv import load_dotenv
import time

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
REREAD_ON_QUERY = os.getenv('REREAD_ON_QUERY').lower() == 'true'

def read_file(file_path):
    """
    Reads the content of the file and returns it as a list of lines.
    :param file_path: The path to the file to read.
    :return: A list of lines from the file.
    """
    with open(file_path, 'r') as file:
        return file.readlines()

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
        search_string = data.decode('utf-8').rstrip('\x00').strip()
        print(f"[INFO] Searching for string: '{search_string}' in the file: {file_path}")

        start_time = time.time()
        # Re-read the file or use cached content based on REREAD_ON_QUERY
        if REREAD_ON_QUERY:
            file_lines = read_file(file_path)
        else:
            if not hasattr(handle_client, "cached_lines"):
                handle_client.cached_lines = read_file(file_path)
            file_lines = handle_client.cached_lines
        
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000

        # Log execution time
        # debug_info = (
        #     f"DEBUG: [TIME: {time.strftime('%Y-%m-%d %H:%M:%S')}] "
        #     f"[IP: {address[0]}] [Query: '{search_string}'] [Execution Time: {elapsed_time:.2f} ms]\n"
        # )

        # Search for a full line match
        if any(line.strip() == search_string for line in file_lines):
            response = "STRING EXISTS\n"
        else:
            response = "STRING NOT FOUND\n"
        
        # Send the response to the client
        client_socket.sendall(response.encode('utf-8'))

        
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
