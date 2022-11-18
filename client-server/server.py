import socket
from threading import Thread
import sys

sys.path.append("../parallel/")
sys.path.append("../")

from util import SERVER_IP_ADDRESS, SERVER_PORT, SERVER_MAX_CONNECTIONS_NUMBER, \
    SERVER_CONNECTION_RESPONSE, ENCODING, clean_line, receive_message, send_message
from parallel.ParallelInvertedIndex import ParallelInvertedIndex

def client_thread(connection, address, hashtable):
    send_message(connection, bytes(SERVER_CONNECTION_RESPONSE, encoding=ENCODING))

    while True:
        try:
            message = receive_message(connection)
            if message:
                stringigied_message = message.decode(ENCODING)
                print(f"{address[0]}:{address[1]}> {stringigied_message}")

                cleaned_message = clean_line(stringigied_message)
                respond = ""
                for word in cleaned_message:
                    respond += str(hashtable[word]).replace(" ", "")
                if len(cleaned_message) == 0:
                    respond = "Nothing has come!"
                try:
                    send_message(connection, bytes(respond, encoding=ENCODING))
                except:
                    remove(connection, address)
            else:
                remove(connection, address)
        except:
            remove(connection, address)
            break

def remove(connection, address):
    connection.close()
    if connection in client_list:
        client_list.remove(connection)
    print(f"Connection removed for {address[0]}:{address[1]}")

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
        connection, address = server.accept()
        client_list.append(connection)

        print(f"{address[0]}:{address[1]} connected")

        thread = Thread(target=client_thread, args=(connection, address, inverted_index))
        thread.start()