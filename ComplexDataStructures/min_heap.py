class MinHeap:
    def __init__(self):
        self.heap_list = [None]
        self.count = 0
        self.swaps_num = 0

    def parent_idx(self, idx):
        return idx // 2

    def child_present(self, idx):
        return self.left_child_idx(idx) <= self.count

    def left_child_idx(self, idx):
        return idx * 2

    def right_child_idx(self, idx):
        return idx * 2 + 1

    def get_smaller_child_idx(self, idx):
        left_child_idx = self.left_child_idx(idx)
        right_child_idx = self.right_child_idx(idx)
        if right_child_idx > self.count:
            return left_child_idx
        left_child = self.heap_list[left_child_idx]
        right_child = self.heap_list[right_child_idx]
        if left_child < right_child:
            return left_child_idx
        return right_child_idx

    def add(self, element):
        self.count += 1
        self.heap_list.append(element)
        self.heapify_up()

    def heapify_up(self):
        idx = self.count
        parent_idx = self.parent_idx(idx)
        while parent_idx > 0:
            child = self.heap_list[idx]
            parent = self.heap_list[parent_idx]
            if parent > child:
                self.swaps_num += 1
                self.heap_list[idx], self.heap_list[parent_idx] = self.heap_list[parent_idx], self.heap_list[idx]
            idx = self.parent_idx(idx)
            parent_idx = self.parent_idx(idx)

    def heapify_down(self):
        idx = 1
        while self.child_present(idx):
            smaller_child_idx = self.get_smaller_child_idx(idx)
            child = self.heap_list[smaller_child_idx]
            parent = self.heap_list[idx]
            if parent > child:
                self.swaps_num += 1
                self.heap_list[smaller_child_idx], self.heap_list[idx] = self.heap_list[idx], self.heap_list[
                    smaller_child_idx]
            idx = smaller_child_idx

    def retrieve_min(self):
        if self.count == 0:
            return None
        min_val = self.heap_list[1]
        self.heap_list[1], self.heap_list[self.count] = self.heap_list[self.count], self.heap_list[1]
        self.heap_list = self.heap_list[:-1]
        self.count -= 1
        self.heapify_down()
        return min_val
