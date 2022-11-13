import numpy as np

P = 41
M = 10**9 + 9

class HashMap:
    def __init__(self, size):
        self.size = size
        self.arr = np.empty((size,), dtype=object)
        for i in range(size):
            self.arr[i] = []

    @staticmethod
    def hash_value(string):
        if type(string) != str:
            raise Exception("Argument should be a string!")
        sum = 0
        for i, char in enumerate(string):
            if char.isdigit():
                char_number = ord('z') - ord('a') + 1 + int(char)
            else:
                char_number = ord(char) - ord('a') + 1
            sum += char_number * pow(P, i, M)
        sum = sum % M
        return sum

    def put(self, key, value):
        position = HashMap.hash_value(key) % self.size
        list_keys_values = self.arr[position]
        for i, pair in enumerate(list_keys_values):
            _key, values = pair
            if _key == key:
                list_keys_values[i][1].append(value)
                self.arr[position] = list_keys_values
                return
        list_keys_values.append((key, [value]))
        self.arr[position] = list_keys_values

    def __setitem__(self, key, values):
        position = HashMap.hash_value(key) % self.size
        list_keys_values = self.arr[position]
        for i, pair in enumerate(list_keys_values):
            _key, _values = pair
            if _key == key:
                list_keys_values[i] = (_key, values)
                self.arr[position] = list_keys_values
                return
        list_keys_values.append((key, values))
        self.arr[position] = list_keys_values

    def get(self, key):
        position = HashMap.hash_value(key) % self.size
        list_keys_values = self.arr[position]
        for _key, values in list_keys_values:
            if _key == key:
                return values
        return []

    def __getitem__(self, item):
        return self.get(item)

    def __str__(self):
        stringified = ""
        for hash_list in self.arr:
            for key, values in hash_list:
                stringified += f"{key}: {values}, "
        return stringified

if __name__ == '__main__':
    map = HashMap(2)
    print(HashMap.hash_value('a'))
    print(HashMap.hash_value('aa'))
    print(HashMap.hash_value('aaa'))
    print(HashMap.hash_value('asdasd'))
    print(HashMap.hash_value('asiodj'))
    print(HashMap.hash_value('ioqweioqw'))
    map.put('asdasd', 'asdasdasd')
    map.put('asiodj', (123, '1232'))
    map.put('ioqweioqw', 'ass')
    map.put('ioqweioqw', 'иss')
    map['asdasd'].append('91029')
    map['asdasd'] = map['asdasd'] + ['9290209']
    print(map['ioqweioqw'])
    print(map['asiodj'])
    print(map['asdasd'])
    print(map)