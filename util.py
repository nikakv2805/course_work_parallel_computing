import re
import string
import sys
import math

SERVER_IP_ADDRESS = "127.0.0.1"
SERVER_PORT = 531
SERVER_MAX_CONNECTIONS_NUMBER = 100
SERVER_CONNECTION_RESPONSE = "Hi! You can now enter your request for index!"
PACKET_SIZE = 65536
INT_ORDER = "big"

ENCODING = "utf-8"

TAGS_PATTERN = re.compile('<.*?>')
MAPPING_TABLE = str.maketrans('', '', string.punctuation)

def clean_line(line):
    splitted_line = re.sub(TAGS_PATTERN, '', line.lower()).split()
    cleaned_line = list(map(lambda w: w.translate(MAPPING_TABLE), splitted_line))
    return cleaned_line

def receive_message(connection):
    packets_count = int.from_bytes(connection.recv(4), INT_ORDER, signed=False)

    if packets_count == 0:
        raise Exception("There should be at least 1 package")

    full_message = b""
    for p in range(packets_count):
        full_message += connection.recv(PACKET_SIZE)
    return full_message

def send_message(connection, message: bytes):
    string_size = sys.getsizeof(b"")
    message_length = sys.getsizeof(message) - string_size
    packets_count = math.ceil(message_length / (PACKET_SIZE - string_size))

    connection.send(packets_count.to_bytes(length=4, byteorder=INT_ORDER, signed=False))

    for p in range(packets_count):
        packet = message[p*(PACKET_SIZE - string_size):min(len(message), (p+1)*(PACKET_SIZE - string_size))]
        connection.send(packet)