import re
import string

SERVER_IP_ADDRESS = "127.0.0.1"
SERVER_PORT = 531
SERVER_MAX_CONNECTIONS_NUMBER = 100
SERVER_CONNECTION_RESPONSE = "Hi! You can now enter your request for index!"

ENCODING = "utf-8"

TAGS_PATTERN = re.compile('<.*?>')
MAPPING_TABLE = str.maketrans('', '', string.punctuation)

def clean_line(line):
    splitted_line = re.sub(TAGS_PATTERN, '', line.lower()).split()
    cleaned_line = list(map(lambda w: w.translate(MAPPING_TABLE), splitted_line))
    return cleaned_line