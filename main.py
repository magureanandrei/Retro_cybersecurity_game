import socket
from threading import Thread


def handle_client(client_socket):
    with open("info.txt", "r") as f:
        data = f.read()
    client_socket.send(data.encode())
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12346))  # Ascultă pe portul 12345
    server.listen(5)
    print("[SERVER] Server pornit, aștept conexiuni...")

    while True:
        client_socket, addr = server.accept()
        print(f"[CONEXIUNE] Conexiune primită de la {addr}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


start_server()