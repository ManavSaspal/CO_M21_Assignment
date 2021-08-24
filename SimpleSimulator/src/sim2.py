import bin_encoding2
import sys
import matplotlib.pyplot as plt


# MEMORY IS BINARY STRING
memory = []

# REGISTERS ARE DECIMAL INTEGERS
# flag = 1 (equal) , 2 (greater),3 (less than) , 4 (overflow)
registers = [0, 0, 0, 0, 0, 0, 0, 0]

# PROGRAM COUNTER
PC = 0


def EE(instruction):
    # type of intruction?
    # send to type function

    operation = bin_encoding2.opcodes[instruction[0:5]]
    type = bin_encoding2.typecodes[operation]

    if type == "A":

        updated_PC = type_A(instruction)

    elif type == "B":

        updated_PC = type_B(instruction)

    elif type == "C":

        updated_PC = type_C(instruction)

    elif type == "D":

        updated_PC = type_D(instruction)

    elif type == "E":
        updated_PC = type_E(instruction)

    elif type == "F":
        reset_flag()
        return (True, PC)

    return (False, updated_PC)


def input_memory():
    for line in sys.stdin:
        if line[-1] == '\n':
            memory.append(line[:-1])
        else:
            memory.append(line)

    while len(memory) < 256:
        memory.append("0000000000000000")


def updatePC(new_PC):
    global PC
    PC = new_PC


def getData(PC):
    # print(PC)
    # print(memory)
    return memory[PC]


def dumpPC():
    out = str(bin(PC)[2:])
    out = ("0" * (16 - len(out))) + out
    print(out, end=" ")


def dumpRF():
    for number in registers:
        out = str(bin(number)[2:])
        out = ("0" * (16 - len(out))) + out
        print(out, end=" ")
    print()


def dumpMEM():
    for line in memory:
        print(line)


# resets FLAG registor
def reset_flag():
    registers[7] = 0
    return


def type_A(instruction):
    flag = registers[7]
    reset_flag()
    # update value of memory and register file according to instruction.
    # returns updated pc
    pass


def type_B(instruction):
    flag = registers[7]
    reset_flag()
    # update value of memory and register file according to instruction.
    # returns updated pc
    pass


def type_C(instruction):
    flag = registers[7]
    reset_flag()
    # update value of memory and register file according to instruction.
    # returns updated pc
    pass


def type_D(instruction):
    flag = registers[7]
    reset_flag()
    # update value of memory and register file according to instruction.
    # returns updated pc
    pass


def type_E(instruction):
    # update value of memory and register file according to instruction.
    # returns updated pc

    flag = registers[7]
    reset_flag()

    addr = instruction[8:16]
    addr = int(addr, 2)
    operation = bin_encoding2.opcodes[instruction[0:5]]

    if operation == "jmp":
        return addr

    if operation == "jgt":

        if flag == 2:
            return addr

    if operation == "jlt":
        if flag == 3:
            return addr

    if operation == "je":
        if flag == 1:
            return addr

    return PC + 1


def main():
    global memory
    global registers
    global PC                   # Start from the first instruction

    input_memory()     # Load memory from stdin
    # print('==========MEMORY LOADED=========')
    # print(memory)
    halted = False

    while not halted:
        print("another iteration")
        # Get current instruction
        instruction = getData(PC)

        # Update RF compute new_PC
        halted, new_PC = EE(instruction)
        
        # Print PC
        dumpPC()
        
        # Print RF state
        dumpRF()
        
        # Update PC
        updatePC(new_PC)

    # Print memory state
    dumpMEM()


if __name__ == "__main__":
    main()
