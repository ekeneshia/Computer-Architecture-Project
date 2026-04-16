#Ekene Okeke Project 4 : Processor 

from programcounter import ProgramCounter
from im import InstructionMemory
from register_file import RegisterFile
from alu import ALU
from control_unit import ControlUnit
from datamemory import DataMemory

def main():
  
    pc_unit = ProgramCounter()
    im = InstructionMemory()
    rf = RegisterFile()
    alu = ALU()
    cu = ControlUnit()
    # dm = DataMemory() # We are not using the data memory

    # Initial values  A=12, B=10, C=15, D=5
    rf.registers['t0'] = 12  # A
    rf.registers['t1'] = 10  # B
    rf.registers['t2'] = 15  # C
    rf.registers['t3'] = 5   # D

    print(" 32-bit Single-Cycle Processor Execution ")
    
    while True:
        curr_pc = pc_unit.get_pc()
        instr = im.fetch(curr_pc)
        if not instr: 
            break

            
        opcode, rd, rs, rt, funct = instr
        signals = cu.decode(opcode, funct)

   
        val_rs, val_rt = rf.read(rs, rt)
        
     
        alu_out = alu.execute(val_rs, val_rt, signals["alu_op"], signals["inv_flag"])

      
        rf.write(rd, alu_out, signals["reg_write"])

        print(f"PC {curr_pc}: {opcode} {rd}, {rs}, {rt} | Result: {hex(alu_out)}")
       
        print(f"Control Signals: ALU_Op={signals['alu_op']}, Inv={signals['inv_flag']}, RegWrite={signals['reg_write']}")
        pc_unit.update()
        reg_state = ", ".join([f"{r}: {hex(rf.registers.get(r, 0))}" for r in ['t0', 't1', 't2', 't3', 't4', 't6']])
        print(f"Register File State: {reg_state}")
        print("-" * 60) # Visual separator

   
    print(f"\nFinal Result Y (t0): {hex(rf.registers['t0'])}")

if __name__ == "__main__":
    main()