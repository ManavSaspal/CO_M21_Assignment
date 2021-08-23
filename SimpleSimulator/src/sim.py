memory = []
registers = []
PC = 0


def type_A():
    # update memory and registers accordingly
    # return halted and new_PC
    # reset flags before an instruction sets flags
    pass

# 6 fucntions
#
# 
# symbol table (opposite to the one in assembler)


def EE(instruction):
    # type of intruction?
    # send to type function
    # 

    pass


def input_memory():
    pass


def input_registers():
    pass


def updatePC(new_PC):
    global PC 
    PC = new_PC


def getData(PC):
    pass


def dumpPC():
    pass


def dumpRF():
    pass


def dumpMEM():
    pass


def main():
    global memory
    global registers
    global PC                                       # Start from the first instruction

    mem = input_memory()                            # Load memory from stdin
    registers = input_registers()
    halted = False

    while not halted:
        instruction = getData(PC);                  # Get current instruction
        halted, new_PC = EE(instruction);           # Update RF compute new_PC
        dumpPC();                                   # Print PC
        dumpRF();                                   # Print RF state
        updatePC(new_PC);                           # Update PC

    dumpMEM()
    # Print memory state


    


if __name__ == "__main__":
    main()