from ComplexDataStructures.blossom_lib import flower_definitions
from ComplexDataStructures.linked_list import LinkedList, Node


class HashMap:
    def __init__(self, size):
        self.array_size = size
        self.array = [LinkedList() for i in range(size)]

    def hash(self, key):
        return sum(key.encode())

    def compress(self, hash_code):
        return hash_code % self.array_size

    def assign(self, key, value):
        array_index = self.compress(self.hash(key))
        payload = Node([key, value])
        list_at_array = self.array[array_index]
        for i in list_at_array:
            if key == i[0]:
                i[1] = value
                return
        list_at_array.insert(payload)

    def retrieve(self, key):
        array_index = self.compress(self.hash(key))
        list_at_index = self.array[array_index]
        for i in list_at_index:
            if key == i[0]:
                return i[1]
        return None


if __name__ == '__main__':
    blossom = HashMap(len(flower_definitions))
    for flower in flower_definitions:
        blossom.assign(flower[0], flower[1])

    print(blossom.retrieve('daisy'))
