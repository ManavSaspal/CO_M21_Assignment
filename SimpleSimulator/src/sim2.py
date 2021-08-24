import bin_encoding2
import sys
import numpy as np

# import matplotlib.pyplot as plt


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
    # print("here in EE()")
    # print("instruction", instruction[0:5])

    operation = bin_encoding2.opcodes[instruction[0:5]]
    if operation == "mov":
        if instruction[0:5] == "00010":
            type = "B"
        else:
            type = "C"
    else:
        type = bin_encoding2.typecodes[operation]

    # print("type is ", type)

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
        if line[-1] == "\n":
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


def getbin(x):
    out = bin(x)[2:]
    out = out[-16:]
    return "0" * (16 - len(out)) + out


def dumpPC():
    out = bin(PC)[2:][-8:]
    print("0" * (8 - len(out)) + out, end=" ")


def dumpRF():
    for number in registers:
        out = getbin(number)
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
    operation = bin_encoding2.opcodes[instruction[0:5]]
    reg1 = instruction[7:10]
    reg1 = int(reg1, 2)
    reg2 = instruction[10:13]
    reg2 = int(reg2, 2)
    reg3 = instruction[13:]
    reg3 = int(reg3, 2)

    if operation == "add":
        registers[reg1] = registers[reg2] + registers[reg3]
        if registers[reg1] > 2 ** 8 - 1:
            registers[7] = 4

    if operation == "sub":
        registers[reg1] = registers[reg2] - registers[reg3]
        if registers[reg3] > registers[reg2]:
            registers[7] = 4

    if operation == "mul":
        registers[reg1] = registers[reg2] * registers[reg3]
        if registers[reg1] > 2 ** 8 - 1:
            registers[7] = 4

    if operation == "xor":
        registers[reg1] = np.bitwise_xor(registers[reg2], registers[reg3])

    if operation == "or":
        registers[reg1] = np.bitwise_or(registers[reg2], registers[reg3])

    return PC + 1

    # update value of memory and register file according to instruction.
    # returns updated pc


def type_B(instruction):
    # print("here in type B")
    flag = registers[7]
    reset_flag()
    operation = bin_encoding2.opcodes[instruction[0:5]]
    reg = instruction[5:8]
    reg = int(reg, 2)
    imm = instruction[8:]
    imm = int(imm, 2)

    # print("imm val is", imm)

    if operation == "mov":
        registers[reg] = imm

    if operation == "ls":
        registers[reg] *= 2 ** imm
        registers[reg] = f"{registers[reg]:08b}"[-8:]
        registers[reg] = int(registers[reg], 2)

    if operation == "ls":
        registers[reg] *= 2 ** imm
        registers[reg] = f"{registers[reg]:08b}"[-8:]
        registers[reg] = int(registers[reg], 2)

    return PC + 1


def type_C(instruction):
    flag = registers[7]
    reset_flag()
    operation = bin_encoding2.opcodes[instruction[0:5]]
    reg1 = instruction[10:13]
    reg1 = int(reg1, 2)
    reg2 = instruction[13:]
    reg2 = int(reg2, 2)

    if operation == "mov":
        registers[reg1] = registers[reg2]

    if operation == "div":
        registers[0] = registers[reg1] / registers[reg2]
        registers[1] = registers[reg1] % registers[reg2]

    if operation == "not":
        registers[reg1] = 2 ** 8 - 1 - registers[reg2]

    if operation == "cmp":
        if reg1 < reg2:
            registers[7] = 3
        if reg1 > reg2:
            registers[7] = 2
        if reg1 == reg2:
            registers[7] = 1

    return PC + 1


def type_D(instruction):
    flag = registers[7]
    reset_flag()
    operation = bin_encoding2.opcodes[instruction[0:5]]
    reg = instruction[5:8]
    reg = int(reg, 2)
    mem = instruction[8:]
    mem = int(mem, 2)

    if operation == "ld":
        registers[reg] = memory[mem]

    if operation == "st":
        out = bin(registers[reg])[2:]
        out = "0" * (16 - len(out)) + out
        memory[mem] = out

    return PC + 1


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
    global PC  # Start from the first instruction

    input_memory()  # Load memory from stdin
    # print('==========MEMORY LOADED=========')
    # print(memory)
    halted = False

    while not halted:
        # print("another iteration")
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
