#Ekene Okeke Project 4 : Data Memory File

class DataMemory:
    def __init__(self):
        self.memory = {}

    def access(self, address, write_data, mem_read, mem_write):
        if mem_write:
            self.memory[address] = write_data
        if mem_read:
            return self.memory.get(address, 0)
        return write_data 