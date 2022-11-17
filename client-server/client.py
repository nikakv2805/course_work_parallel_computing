import socket

from util import SERVER_IP_ADDRESS, SERVER_PORT, ENCODING, send_message, receive_message

if __name__ == "__main__":
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.connect((SERVER_IP_ADDRESS, SERVER_PORT))
    print(f"Connected to server on IP ADDRESS {SERVER_IP_ADDRESS}:{SERVER_PORT}")

    try:
        while True:
            server_respond = receive_message(server_connection)
            print(server_respond.decode(ENCODING))

            message = bytes(input(), encoding=ENCODING)
            send_message(server_connection, message)
    except:
        print("Disconecting due to problems...")
        server_connection.close()