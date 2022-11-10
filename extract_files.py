import os
import re
import functools
import shutil

MY_VARIANT = 7
VARIANTS_COUNT = 50
PATH_TO_FOLDERS = "E:/nikak/Курсач_паралельки/datasets"
FOLDERS_FOR_EXTRACTION = [f"{PATH_TO_FOLDERS}/aclImdb/test/neg/", f"{PATH_TO_FOLDERS}/aclImdb/test/pos/",
                          f"{PATH_TO_FOLDERS}/aclImdb/train/neg/", f"{PATH_TO_FOLDERS}/aclImdb/train/pos/",
                          f"{PATH_TO_FOLDERS}/aclImdb/train/unsup/"]
FILE_PATTERN = re.compile("^[0-9]+_[0-9]+\.txt$")
TARGET_FOLDER_PATH = r"./files/"

def decompose_filename(filename):
    if not FILE_PATTERN.match(filename):
        raise Exception("Filename should match the pattern")
    splitter = filename.find('_')
    part1 = int(filename[:splitter])
    part2 = int(filename[splitter+1:-4])
    return part1, part2


def compare(filename1, filename2):
    if type(filename1) != str or type(filename2) != str:
        raise Exception("Filenames should be strings!")
    elif FILE_PATTERN.match(filename1):
        if FILE_PATTERN.match(filename2):
            filename1_p1, filename1_p2 = decompose_filename(filename1)
            filename2_p1, filename2_p2 = decompose_filename(filename2)
            return filename1_p1 - filename2_p1 + (filename1_p1 == filename2_p1) * (filename1_p2 - filename2_p2)
        else:
            return -1
    else:
        if FILE_PATTERN.match(filename2):
            return 1
        else:
            if filename1 < filename2:
                return -1
            elif filename2 < filename1:
                return 1
            else:
                return 0

if __name__ == "__main__":
    for i, folder in enumerate(FOLDERS_FOR_EXTRACTION):
        files_list = list(filter(lambda x: os.path.isfile(os.path.join(folder, x)) and FILE_PATTERN.match(x),
                      os.listdir(folder)))
        files_list.sort(key=functools.cmp_to_key(compare))
        files_count = len(files_list)
        variant_start_file = files_count//VARIANTS_COUNT*(MY_VARIANT - 1)
        variant_end_file = files_count//VARIANTS_COUNT*MY_VARIANT
        my_files_list = files_list[variant_start_file:variant_end_file]
        print(my_files_list)
        for file in my_files_list:
            shutil.copyfile(folder + file, TARGET_FOLDER_PATH + file[:-4] + f"_{i}.txt")