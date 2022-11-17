import socket
import re
import string
from multiprocessing.dummy import Process as Thread

import sys
sys.path.append("../parallel/")

from parallel.ParallelInvertedIndex import ParallelInvertedIndex

IP_ADDRESS = "127.0.0.1"
PORT = 531
MAX_CONNECTIONS_NUMBER = 100

TAGS_PATTERN = re.compile('<.*?>')

def clientthread(conn, addr, hashtable):
    conn.send(b"Hi! You can enter your request for index!")

    mapping_table = str.maketrans('', '', string.punctuation)

    while True:
        try:
            message = conn.recv(2048)
            if message:
                stringigied_message = message.decode("utf-8")
                print(f"{addr[0]}:{addr[1]}> {stringigied_message}")

                splitted_message = re.sub(TAGS_PATTERN, '', stringigied_message.lower()).split()
                cleaned_message = list(map(lambda w: w.translate(mapping_table), splitted_message))
                respond = ""
                for word in cleaned_message:
                    respond += str(hashtable[word])

                try:
                    conn.send(bytes(respond, encoding="utf-8"))
                except:
                    conn.close()
                    remove(conn)
            else:
                remove(conn)
        except:
            continue

def remove(connection):
    if connection in client_list:
        client_list.remove(connection)

if __name__ == '__main__':
    """
    AF_INET - address family of IPv4
    SOCK_STREAM provides sequenced, two-way byte streams with a transmission mechanism for stream data, means TCP/IP
    SOL_SOCKET means we set option only for server solo socket
    SO_REUSEADDR set to 1 allows reuse of local addresses 
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print(f"Starting server on IP ADDRESS {IP_ADDRESS}:{PORT}")
    server.bind((IP_ADDRESS, PORT))

    server.listen(MAX_CONNECTIONS_NUMBER)

    client_list = []

    index = ParallelInvertedIndex()
    inverted_index = index()
    print("Inverted index is created")

    print("Starting to accept new connections")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)

        print(f"{addr[0]}:{addr[1]} connected")

        thread = Thread(target=clientthread, args=(conn, addr, inverted_index))
        thread.start()