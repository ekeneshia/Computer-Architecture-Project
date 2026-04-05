# Processor Design Semester Project - Task 3
# Ekene Okeke
# Memory Hierarchy Simulation (SSD -> DRAM -> Cache)
import random
import time

# Memory Level Configuration 
L1_SIZE = 2
L2_SIZE = 4
L3_SIZE = 8
DRAM_SIZE = 16
SSD_SIZE = 100

class MemoryLevel:
    def __init__(self, name, size, latency, policy):
        self.name = name
        self.max_size = size
        self.latency = latency
        self.policy = policy
        self.data_store = {}     
        self.access_order = []   
        self.hits = 0
        self.misses = 0

    def check_cache(self, addr):
        if addr in self.data_store:
            self.hits += 1
            if self.policy == "LRU":
              
                if addr in self.access_order:
                    self.access_order.remove(addr)
                self.access_order.append(addr)
            return True
        self.misses += 1
        return False

    def insert_data(self, addr, instr):
        if len(self.data_store) >= self.max_size:
            if self.policy == "FIFO" or self.policy == "LRU":
                victim = self.access_order.pop(0)
            else: 
                victim = random.choice(list(self.data_store.keys()))
                if victim in self.access_order:
                    self.access_order.remove(victim)
            
            print(f"    LOG: {self.name} Full! Evicting address {victim}")
            del self.data_store[victim]
        
        self.data_store[addr] = instr
        self.access_order.append(addr)

class ProcessorMemorySystem:
    def __init__(self, repl_policy="LRU"):
        self.l1 = MemoryLevel("L1_Cache", L1_SIZE, 1, repl_policy)
        self.l2 = MemoryLevel("L2_Cache", L2_SIZE, 5, repl_policy)
        self.l3 = MemoryLevel("L3_Cache", L3_SIZE, 20, repl_policy)
        self.dram = MemoryLevel("DRAM", DRAM_SIZE, 100, repl_policy)
        self.ssd = MemoryLevel("SSD", SSD_SIZE, 1000, repl_policy)
        
        self.levels = [self.l1, self.l2, self.l3, self.dram, self.ssd]
        self.clock_cycles = 0

    def request_instruction(self, address):
        print(f"\n Requesting Instruction at {address} ")
        found_at = -1
        for i in range(len(self.levels)):
            self.clock_cycles += self.levels[i].latency
            if self.levels[i].check_cache(address):
                print(f"Hit found at {self.levels[i].name}")
                found_at = i
                break
            else:
                print(f"Miss at {self.levels[i].name}")

        if found_at != -1:
            instruction = self.levels[found_at].data_store[address]
            for j in range(found_at - 1, -1, -1):
                print(f"Moving data: {self.levels[j+1].name} -> {self.levels[j].name}")
                self.levels[j].insert_data(address, instruction)
        
        print(f"Total cycles so far: {self.clock_cycles}")

# Program for demonstrating project as seen beloww
if __name__ == "__main__":
    my_system = ProcessorMemorySystem("LRU")

  
    for a in range(100):
        my_system.ssd.data_store[a] = f"INST_HEX_{a:08X}"
        my_system.ssd.access_order.append(a)

    trace_addresses = [5, 5, 12, 15, 5] 
    
    for addr in trace_addresses:
        my_system.request_instruction(addr)
        time.sleep(0.4)

    print("\n\n")
    print("Final System State Report")

    for lvl in my_system.levels:
        print(f"{lvl.name} | Hits: {lvl.hits} | Misses: {lvl.misses}")
        print(f"  Current Data: {list(lvl.data_store.keys())}")
    print(f"\nTotal Execution Time: {my_system.clock_cycles} Cycles")