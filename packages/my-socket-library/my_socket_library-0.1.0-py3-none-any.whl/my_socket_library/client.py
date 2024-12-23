import socket


def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    try:
        while True:
            message = input("Введите сообщение для сервера: ")
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(2048)
            print(f'Сервер: {data.decode("utf-8")}')
    finally:
        client_socket.close()
