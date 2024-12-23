import socket


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Сервер запущен на {host}:{port}...')
    conn, addr = server_socket.accept()
    print(f'Клиент подключен: {addr}')
    try:
        while True:
            data = conn.recv(2048)
            if not data:
                break
            print(f'Клиент: {data.decode("utf-8")}')
            msg = input('Вы: ')
            if msg == 'end':
                break
            conn.sendall(msg.encode('utf-8'))
    finally:
        conn.close()
        server_socket.close()
