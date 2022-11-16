import os
import re
import string
import time
from multiprocessing import Process, Queue

from ParallelHashMap import ParallelHashMap

TAGS_PATTERN = re.compile('<.*?>')

class ParallelInvertedIndex:
    def __init__(self, processes_count=4):
        self.processes_count = processes_count

    @staticmethod
    def get_data(files_list, folder="../files/"):
        files_data = []
        for file_name in files_list:
            with open(folder + file_name, encoding="utf8") as f:
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
    def create_index(clean_data, dictionary_size):
        dictionary = ParallelHashMap(dictionary_size)
        for file_clean_data, file_name in clean_data:
            for line_num, clean_line in enumerate(file_clean_data):
                for word_num, word in enumerate(clean_line):
                    index = (file_name, line_num, word_num)
                    dictionary.put(word, index)
        return dictionary

    class InvertedSubindex(Process):
        def __init__(self, files_list, queue, dictionary_size=40000):
            super(ParallelInvertedIndex.InvertedSubindex, self).__init__()
            self.files_list = files_list
            self.dictionary_size = dictionary_size
            self.queue = queue

        def run(self):
            files_data = ParallelInvertedIndex.get_data(self.files_list)
            cleaned_data = ParallelInvertedIndex.clean_data(files_data)
            self.queue.put(ParallelInvertedIndex.create_index(cleaned_data, self.dictionary_size))

    def __call__(self, folder="../files/"):
        files_list = list(filter(lambda x: os.path.isfile(os.path.join(folder, x)),
                                 os.listdir(folder)))
        # dividing files from directory to several processes
        files_divided = []
        files_count_on_process = len(files_list) // self.processes_count
        for process_num in range(self.processes_count - 1):
            files_divided.append(files_list[files_count_on_process * process_num:files_count_on_process * (process_num + 1)])
        files_divided.append(files_list[files_count_on_process * (self.processes_count - 1):])
        dict_size = len(files_list) * 20
        queue = Queue()
        processes = []
        for i in range(self.processes_count):
            processes.append(ParallelInvertedIndex.InvertedSubindex(files_divided[i], queue, dict_size))
            processes[i].start()
        dicts = []
        for _ in processes:
            dicts.append(queue.get())
        [proc.join() for proc in processes]
        return_dict = dicts[0]
        for i in range(1, self.processes_count):
            return_dict.unite(dicts[i])
        return return_dict

if __name__ == '__main__':
    for i in range(8):
        start_time = time.time()
        inverted_index = ParallelInvertedIndex(processes_count=i+1)
        index = inverted_index()
        print(f"{i+1} processes takes {time.time() - start_time} seconds")