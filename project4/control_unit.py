#Ekene Okeke Project 4 : Control Unit File

class ControlUnit:
    def decode(self, opcode, funct):
        signals = {
            "reg_write": True,
            "alu_op": "OR" if opcode == "or" else "AND",
            "inv_flag": True if funct == "INV" else False,
            "mem_read": False,
            "mem_write": False
        }
        return signals