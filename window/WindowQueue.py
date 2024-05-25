from collections import deque


class WindowQueue:
    def __init__(self, window_size=-1):
        self.__window_size = window_size
        self.__dequeue = deque()

    @property
    def window_size(self):
        return self.__window_size

    def push(self, element):
        if 0 < self.__window_size == len(self.__dequeue):
            self.__dequeue.popleft()

        self.__dequeue.append(element)

    def push_and_sort(self, element, *args, **kwargs):
        if 0 < self.__window_size == len(self.__dequeue):
            self.__dequeue.popleft()

        self.__dequeue.append(element)
        self.sort(*args, **kwargs)

    def pop(self):
        return self.__dequeue.popleft()

    def get(self):
        return self.__dequeue

    def print(self):
        new_queue = deque(self.__dequeue)
        new_queue.reverse()
        for element in new_queue:
            print(element, end=" ")
        print()

    def sort(self, *args, **kwargs):
        items = [self.__dequeue.pop() for _ in range(len(self.__dequeue))]
        # for element in items:
        #     print(element, end=" ")
        # print()
        items.sort(*args, **kwargs)
        self.__dequeue.extend(items)

    def to_list(self):
        return list(self.__dequeue)

    def __len__(self):
        return len(self.__dequeue)

    def __str__(self):
        return str(self.__dequeue)
