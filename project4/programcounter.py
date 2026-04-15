#Ekene Okeke Project 4 : Program Counter 
class ProgramCounter:
    def __init__(self):
        self.pc = 0

    def update(self):
        self.pc += 1 

    def get_pc(self):
        return self.pc