import socket
from random import randint
from time import sleep

from util import SERVER_IP_ADDRESS, SERVER_PORT, ENCODING

AUTOCLIENT_FILE = "./autoclient_words.txt"
AUTOCLIENT_SLEEP_TIME = 1
MAX_SYMBOLS = 128

if __name__ == "__main__":
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.connect((SERVER_IP_ADDRESS, SERVER_PORT))
    print(f"Connected to server on IP ADDRESS {SERVER_IP_ADDRESS}:{SERVER_PORT}")

    with open(AUTOCLIENT_FILE, "r", encoding=ENCODING) as file:
        lines = file.readlines()
    lines_count = len(lines)
    print("Queries collected")

    try:
        while True:
            server_respond = server_connection.recv(65536)
            print(f"Server respond is: {server_respond.decode(ENCODING)}")

            sleep(AUTOCLIENT_SLEEP_TIME)

            query = lines[randint(0, lines_count - 1)][:-1]  # better to remove \n from the end
            while len(query) == 0:
                query = lines[randint(0, lines_count - 1)][:-1]
            if len(query) > MAX_SYMBOLS:
                query = query[:MAX_SYMBOLS]
            print(f"Query is: {query}")
            message = bytes(query, encoding=ENCODING)
            server_connection.send(message)

    except:
        print("Disconecting due to problems...")
        server_connection.close()