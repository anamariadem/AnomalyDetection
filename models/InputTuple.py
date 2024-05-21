class InputTuple:
    def __init__(self, id):
        self.__id = id
        self.__in_time = -1
        self.__out_time = -1
        self.__cpu_percentage = -1
        self.__memory_percentage = -1
        self.__processed = False

    @property
    def id(self):
        return self.__id

    @property
    def in_time(self):
        return self.__in_time

    @property
    def out_time(self):
        return self.__out_time

    @property
    def cpu_percentage(self):
        return self.__cpu_percentage

    @property
    def memory_percentage(self):
        return self.__memory_percentage

    @property
    def processed(self):
        return self.__processed

    def set_arrival_time(self, time):
        self.__in_time = time

    def set_output_time(self, time):
        self.__out_time = time

    def set_cpu_percentage(self, percentage):
        self.__cpu_percentage = percentage

    def set_memory_percentage(self, percentage):
        self.__memory_percentage = percentage

    def set_processed(self, value):
        self.__processed = value

