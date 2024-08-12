# tech-assesment
# Overview
This project is a TCP server that listens for client connections, searches for specific strings in a file, and responds with whether the string exists in the file. It uses Python’s built-in modules for networking and file handling, and it supports both single and multi-threaded operations.

# Features
1. TCP Server: Listens for incoming connections on a specified port.

2. String Search: Searches for exact matches of strings in a file.

3. Configuration: Reads settings from a .env file.

4. Dynamic File Reading: Supports re-reading the file on each query if specified.

5. Debug Logging: Provides detailed debug logs including search queries and execution times.

# Requirements & Dependencies
Ensure Python 3 is installed on your system. Install required Python libraries using pip.  

# Installation
Clone the repository to your local machine using Git:
```
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

# Create and Activate a Virtual Environment
```
virtualvenv .venv
source .venv/bin/activate
```

# To install requirements use: 
```
pip install -r requirements.txt
```

Create a .env file and add your configurations. Use the .envsample to guide you.

# Usage
1. Start the Server: Run the server script to start listening for client connections.

```
python server.py
```
2. Connect to the Server: Use a TCP client to connect to the server and send search queries. In my case i used telnet
```
telnet 127.0.0.1 8000
```

# Troubleshooting
1. File Not Found: Ensure that the path in the .env and config.txt files is correct and accessible.

2. Connection Issues: Verify that the server is running and listening on the correct port. Check firewall settings if necessary.

# Contributing
Fork the repository and create a new branch.

Make your changes and test them thoroughly.

Submit a pull request with a detailed description of your changes.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

