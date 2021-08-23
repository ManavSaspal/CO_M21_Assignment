import bin_encoding2


memory = []
registers = [0,0,0,0,0,0,0,0]
#registor is a list of integers
# flag = 1 (equal) , 2 (greater),3 (less than) , 4 (overflow)
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
        return (True , PC )

    return (False,updated_PC)


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

def reset_flag():
    
    # resets FLAG registor
    registers[7]=0 
    return

def type_A(instruction):
    flag = registers[7]    
    reset_flag()
    #update value of memory and register file according to instruction.
    # returns updated pc
    pass

def type_B(instruction):
    flag = registers[7]    
    reset_flag()
    #update value of memory and register file according to instruction.
    # returns updated pc
    pass

def type_C(instruction):
    flag = registers[7]    
    reset_flag()
    #update value of memory and register file according to instruction.
    # returns updated pc
    pass

def type_D(instruction):
    flag = registers[7]    
    reset_flag()
    #update value of memory and register file according to instruction.
    # returns updated pc
    pass

def type_E(instruction):
    #update value of memory and register file according to instruction.
    # returns updated pc
    
    flag = registers[7]    
    reset_flag()

    addr = instruction[8:16] 
    addr = int(addr,2)
    operation = bin_encoding2.opcodes[instruction[0:5]]
    
    if(operation == "jmp"):
        return addr

    if(operation == "jgt"):
        
        if(flag==2):
           return addr 

    if(operation == "jlt" ):
        if(flag == 3):
            return addr

    if(operation == "je"):
        if(flag== 1):
            return addr

    return PC+1
    


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