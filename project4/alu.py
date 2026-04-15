#Ekene Okeke Project 4 : ALU File

class ALU:
    def execute(self, rs_val, rt_val, alu_op, inv_signal):
   
        a_input = (rs_val ^ 0xFFFFFFFF) if inv_signal else rs_val
        b_input = rt_val
        
    
        if alu_op == "OR":
            result = a_input | b_input
        else: # AND
            result = a_input & b_input
            
        return result & 0xFFFFFFFF