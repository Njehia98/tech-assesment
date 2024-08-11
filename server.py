import socket
import threading

# Define the server host and port
HOST = '127.0.0.1'  # localhost
PORT = 12345        # Arbitrary non-privileged port
CONFIG_FILE = 'config.txt'  # Path to your configuration file

def get_linux_path(config_file):
    """
    Reads the configuration file and extracts the linux path.
    :param config_file: The path to the configuration file.
    :return: The path specified in the line starting with 'linuxpath='.
    """
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('linuxpath='):
                # Extract the path after 'linuxpath='
                linux_path = line.split('=', 1)[1].strip()
                return linux_path
    return None

def handle_client(client_socket, address, file_path):
    """
    Function to handle client connections.
    :param client_socket: The socket object for the client connection.
    :param address: The address of the client.
    :param file_path: The path to the file specified in the configuration.
    """
    print(f"[INFO] Connection established with {address}")
    
    try:
        # Send the file contents to the client
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        client_socket.sendall(file_content.encode('utf-8'))
    
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
    # Get the path from the configuration file
    file_path = get_linux_path(CONFIG_FILE)
    
    if not file_path:
        print("[ERROR] 'linuxpath=' not found in the configuration file.")
        return
    
    print(f"[INFO] File path from config: {file_path}")
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow address reuse
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen()
    print(f"[INFO] Server listening on {HOST}:{PORT}")
    
    while True:
        # Accept incoming connections
        client_socket, address = server_socket.accept()
        
        # Create a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, file_path))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()
