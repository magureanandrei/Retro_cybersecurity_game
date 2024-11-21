import socket
import pickle  # For serializing the data (list of files)


# The directory server listens for clients that request a list of available files.
def handle_client(client_socket):
    # Server 2's IP and port (Client A).
    server_2_ip = '192.168.35.236'  # The IP address of Client A
    server_2_port = 12346  # The port of Client A's file server

    # Send the client the address of Server 2 (Client A) and available files
    file_list = ["file1.txt", "file2.txt", "file3.txt"]  # Example file list

    client_socket.send("Available files: \n".encode())
    for filename in file_list:
        client_socket.send(f"{filename}\n".encode())

    # Request file from Client B to fetch from Server 2
    client_socket.send("[INFO] Enter the file name you want to download: ".encode())
    file_request = client_socket.recv(1024).decode().strip()

    # Check if the file exists in the list
    if file_request in file_list:
        client_socket.send(
            f"[INFO] File {file_request} is available. Connecting you to the file server (Server 2)...".encode())
        # Send the IP and port of Server 2 (Client A)
        server_2_address = f"{server_2_ip}:{server_2_port}"
        client_socket.send(f"{server_2_address}\n".encode())
    else:
        client_socket.send("[ERROR] File not found on the server.".encode())

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12346))  # Listening on all interfaces
    server.listen(5)
    print("[SERVER 1] Directory Server started. Waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"[SERVER 1] Connection from {addr}")
        handle_client(client_socket)


start_server()
