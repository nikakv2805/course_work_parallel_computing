import socket

IP_ADDRESS = "127.0.0.1"
PORT = 531

if __name__ == "__main__":
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.connect((IP_ADDRESS, PORT))
    print(f"Connected to server on IP ADDRESS {IP_ADDRESS}:{PORT}")

    try:
        while True:
            server_respond = server_connection.recv(2048)
            print(server_respond.decode("utf-8"))

            message = bytes(input(), encoding="utf-8")
            server_connection.send(message)
    except:
        print("Disconecting due to problems...")
        server_connection.close()