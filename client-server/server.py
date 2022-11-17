import socket
from multiprocessing.dummy import Process as Thread
import sys

sys.path.append("../parallel/")

from util import SERVER_IP_ADDRESS, SERVER_PORT, SERVER_MAX_CONNECTIONS_NUMBER, \
    SERVER_CONNECTION_RESPONSE, ENCODING, clean_line
from parallel.ParallelInvertedIndex import ParallelInvertedIndex

def client_thread(conn, addr, hashtable):
    conn.send(bytes(SERVER_CONNECTION_RESPONSE, encoding=ENCODING))

    while True:
        try:
            message = conn.recv(2048)
            if message:
                stringigied_message = message.decode(ENCODING)
                print(f"{addr[0]}:{addr[1]}> {stringigied_message}")

                cleaned_message = clean_line(stringigied_message)
                respond = ""
                for word in cleaned_message:
                    respond += str(hashtable[word])

                try:
                    conn.send(bytes(respond, encoding=ENCODING))
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

    print(f"Starting server on IP ADDRESS {SERVER_IP_ADDRESS}:{SERVER_PORT}")
    server.bind((SERVER_IP_ADDRESS, SERVER_PORT))

    server.listen(SERVER_MAX_CONNECTIONS_NUMBER)

    client_list = []

    index = ParallelInvertedIndex()
    inverted_index = index()
    print("Inverted index is created")

    print("Starting to accept new connections")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)

        print(f"{addr[0]}:{addr[1]} connected")

        thread = Thread(target=client_thread, args=(conn, addr, inverted_index))
        thread.start()