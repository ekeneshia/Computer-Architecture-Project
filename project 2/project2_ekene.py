#EKene Okeke project 2
# Spring 2026 Computer Architecture 

# What I have implemented:
# User can input the variable number 
# can choose from
import itertools


n = int(input("Enter number of variables (>=2): "))

if n < 2:
    print("Need at least 2 variables")
    exit()

rows = 2 ** n

print("Enter truth table rows (inputs then output)")
print("Example for 3 variables would be typed like this: 0 1 1 0")

table = []
seen = []

for i in range(rows):

    data = input("Row " + str(i+1) + ": ").split()

    if len(data) != n + 1:
        print("Wrong format")
        exit()

    inputs = tuple(map(int, data[:n]))
    output = int(data[-1])

    if inputs in seen:
        print("Duplicate input combination")
        exit()

    if output not in [0,1]:
        print("Output must be 0 or 1")
        exit()

    seen.append(inputs)
    table.append((inputs, output))


# Printing Truth Table

print("\nTruth Table")
for r in table:
    print(r[0], "->", r[1])



vars = []
for i in range(n):
    vars.append(chr(ord('A') + i))


#allows to choose whether you want SOP or POS

form = input("\nChoose form (SOP or POS): ").upper()


#finds the SOP

if form == "SOP":

    minterms = []
    terms = []

    for i in range(len(table)):

        inputs, out = table[i]

        if out == 1:

            minterms.append(i)

            term = ""

            for j in range(n):

                if inputs[j] == 1:
                    term += vars[j]
                else:
                    term += vars[j] + "'"

            terms.append(term)

    canonical = " + ".join(terms)

    print("\nCanonical SOP:")
    print(canonical)

    print("Minterms:", minterms)


# finds the POS

elif form == "POS":

    maxterms = []
    terms = []

    for i in range(len(table)):

        inputs, out = table[i]

        if out == 0:

            maxterms.append(i)

            term = []

            for j in range(n):

                if inputs[j] == 0:
                    term.append(vars[j])
                else:
                    term.append(vars[j] + "'")

            terms.append("(" + " + ".join(term) + ")")

    canonical = "".join(terms)

    print("\nCanonical POS:")
    print(canonical)

    print("Maxterms:", maxterms)

else:
    print("Invalid choice")
    exit()


# K Maps creation section

print("\nK-Map")


values = [r[1] for r in table]

if n == 2:
   
    kmap = [
        [values[0], values[1]],  
        [values[2], values[3]]  
    ]
    
    print("      B")
    print("     0 1")
    print("A 0  ", kmap[0][0], kmap[0][1])
    print("A 1  ", kmap[1][0], kmap[1][1])

elif n == 3:

    kmap = [
        [values[0], values[1], values[3], values[2]],  # A=0
        [values[4], values[5], values[7], values[6]]   # A=1
    ]
    
    print("        BC")
    print("       00 01 11 10")
    print("A=0   ", *kmap[0])
    print("A=1   ", *kmap[1])

elif n == 4:
    
    kmap = [
        [values[0],  values[1],  values[3],  values[2]],  # AB=00
        [values[4],  values[5],  values[7],  values[6]],  # AB=01
        [values[12], values[13], values[15], values[14]], # AB=11
        [values[8],  values[9],  values[11], values[10]]  # AB=10
    ]
    
    print("        CD")
    print("        00 01 11 10")
    print("      -------------")
    print("AB=00 |", *kmap[0])
    print("AB=01 |", *kmap[1])
    print("AB=11 |", *kmap[2])
    print("AB=10 |", *kmap[3])

else:
    print("K-map simplification only supported for 2 - 4 variables")

# functions to help simplify either the SOP or the POS
def simplify_SOP(table, n, vars):
    
    minterms = [i for i, val in enumerate(table) if val == 1]
    if not minterms: return "0"
    if len(minterms) == 2**n: return "1"
    
 
    prime_implicants = run_reduction(minterms, n)
    
   
    final_terms = []
    for p in sorted(list(prime_implicants)):
        term = ""
        for i in range(n):
            if p[i] == '1': term += vars[i]
            elif p[i] == '0': term += vars[i] + "'"
        final_terms.append(term if term else "1")
    return " + ".join(final_terms)


def simplify_POS(table, n, vars):
  
    maxterms = [i for i, val in enumerate(table) if val == 0]
    if not maxterms: return "1"
    if len(maxterms) == 2**n: return "0"
    

    prime_implicants = run_reduction(maxterms, n)
    
    
    final_terms = []
    for p in sorted(list(prime_implicants)):
        parts = []
        for i in range(n):
           
            if p[i] == '0': parts.append(vars[i])
            elif p[i] == '1': parts.append(vars[i] + "'")
        final_terms.append("(" + " + ".join(parts) + ")")
    return "".join(final_terms)

def run_reduction(indices, n):
    """Helper to find the smallest set of terms using bit-comparison."""
    current_terms = set(bin(i)[2:].zfill(n) for i in indices)
    all_primes = set()
    
    while current_terms:
        new_terms = set()
        merged = set()
        list_terms = list(current_terms)
        for i in range(len(list_terms)):
            for j in range(i + 1, len(list_terms)):
                t1, t2 = list_terms[i], list_terms[j]
             
                diffs = [k for k in range(n) if t1[k] != t2[k]]
                if len(diffs) == 1:
                    idx = diffs[0]
                    new_terms.add(t1[:idx] + '-' + t1[idx+1:])
                    merged.add(t1)
                    merged.add(t2)
        all_primes.update(current_terms - merged)
        current_terms = new_terms
    return all_primes

# we find the simplified expression by calling the function

simplified = simplify_SOP(values, n, vars) if form == "SOP" else simplify_POS(values, n, vars)

print("\nSimplified Expression:")
print(simplified)


#Validating the simplified expression

valid = True

for i in range(len(table)):

    original_output = table[i][1]
   
    processed_output = values[i]


    if original_output != processed_output:
        valid = False
        print(f"Row {i+1}: Mismatch found! {original_output} vs {processed_output}")
    else:
 
        print(f"Row {i+1}: Input {table[i][0]} : Output {original_output} [MATCH]")

if valid:
    print("\nValidation Result: PASS")
    print("The simplified expression is equal to the truth table.")
else:
    print("\nValidation Result: FAIL")

