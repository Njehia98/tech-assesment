import socket
import threading
import os
from dotenv import load_dotenv
import time

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
SERVER_NAME = os.getenv('SERVER_NAME')
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS'))
LOG_LEVEL = os.getenv('LOG-LEVEL')
LINUX_PATH = os.getenv('LINUXPATH')
TIMEOUT = int(os.getenv('TIMEOUT'))
DEBUG_MODE = os.getenv('DEBUG_MODE').lower() == 'true'
REREAD_ON_QUERY = os.getenv('REREAD_ON_QUERY').lower() == 'true'

def search_string_in_server(search_string):
    """
    Connects to the server, sends the search string, and prints the response.
    :param search_string: The string to search for in the server file.
    """
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((HOST, PORT))
            print(f"[INFO] Connected to server {HOST}:{PORT}")

            # Send the search string to the server
            s.sendall(search_string.encode('utf-8'))
            print(f"[INFO] Sent search string: '{search_string}'")

            # Receive the response from the server
            response = s.recv(1024).decode('utf-8')
            print(f"[INFO] Received response from server: {response}")

    except ConnectionRefusedError:
        print("[ERROR] Unable to connect to the server. Is it running?")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

if __name__ == "__main__":
    # Input the string to search
    search_string = input("Enter the string to search for: ")
    search_string_in_server(search_string)
