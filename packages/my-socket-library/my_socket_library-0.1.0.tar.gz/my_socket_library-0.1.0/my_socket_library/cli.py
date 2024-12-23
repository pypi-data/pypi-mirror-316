import argparse
from my_socket_library import start_client, start_server


def main():
    parser = argparse.ArgumentParser(description="Socket Client/Server CLI")
    parser.add_argument("mode", choices=["client", "server"],
                        help="Режим работы (client или server)")
    parser.add_argument("host", help="IP-адрес")
    parser.add_argument("port", type=int, help="Порт")

    args = parser.parse_args()

    if args.mode == "client":
        start_client(args.host, args.port)
    elif args.mode == "server":
        start_server(args.host, args.port)


if __name__ == "__main__":
    main()
