#Ekene Okeke Project 4 : Register File

class RegisterFile:
    def __init__(self):
        self.registers = {f"t{i}": 0 for i in range(32)}

    def read(self, rs, rt):
        val_rs = self.registers.get(rs, 0)
        val_rt = self.registers.get(rt, 0)
        return val_rs, val_rt

    def write(self, rd, value, reg_write_en):
        if reg_write_en and rd in self.registers:
            self.registers[rd] = value & 0xFFFFFFFF