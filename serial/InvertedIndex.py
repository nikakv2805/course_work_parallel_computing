import os
import string
import re
from HashMap import HashMap

TAGS_PATTERN = re.compile('<.*?>')

class InvertedIndex:
    def __init__(self, folder="../files/"):
        self.folder = folder

    def get_data(self):
        files_list = list(filter(lambda x: os.path.isfile(os.path.join(self.folder, x)),
                                 os.listdir(self.folder)))
        files_data = []
        for file_name in files_list:
            with open(self.folder + file_name, encoding="utf8") as f:
                file_data = []
                for line in f:
                    file_data.append(line)
                files_data.append((file_data, file_name))
        return files_data

    @staticmethod
    def clean_data(raw_data):
        cleaned_data = []
        mapping_table = str.maketrans('', '', string.punctuation)
        for file_raw_data, file_name in raw_data:
            file_cleaned_data = []
            for line in file_raw_data:
                line_lower = line.lower()
                words = re.sub(TAGS_PATTERN, '', line_lower).split()
                cleaned_words = list(map(lambda w: w.translate(mapping_table), words))
                file_cleaned_data.append(cleaned_words)
            cleaned_data.append((file_cleaned_data, file_name))
        return cleaned_data

    @staticmethod
    def create_index(clean_data):
        dictionary = HashMap(len(clean_data)*20)
        for file_clean_data, file_name in clean_data:
            for line_num, clean_line in enumerate(file_clean_data):
                for word_num, word in enumerate(clean_line):
                    index = (file_name, line_num, word_num)
                    dictionary.put(word, index)
        return dictionary

    def __call__(self):
        files_data = self.get_data()
        # print(files_data)
        cleaned_data = InvertedIndex.clean_data(files_data)
        index = InvertedIndex.create_index(cleaned_data)
        return index

if __name__ == "__main__":
    inverted_index = InvertedIndex()
    index = inverted_index()
    print(index)
    print(index['p'])