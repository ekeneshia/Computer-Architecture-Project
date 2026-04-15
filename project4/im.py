#Ekene Okeke Project 4 : Instruction memory File

# t0=A t1=B t2=C t3=D
class InstructionMemory:
    def __init__(self):

        self.memory = [
            ["and", "t4", "t0", "t1", "STD"], # A & B 
            ["and", "t6", "t2", "t3", "INV"], # ~C & D 
            ["or",  "t0", "t4", "t6", "STD"]  # t4 | t6 
        ]

    def fetch(self, pc):
        if pc < len(self.memory):
            return self.memory[pc]
        return None