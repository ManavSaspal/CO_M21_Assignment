"""


assembler
"""
import sys
import bin_encoding

# =========================================================================
# =============================STORING DATA================================


# Variable dict -> {“variable1”: 00000101} this address is memory location
variables = {}

# Label dict -> {“label1”: 00001111} this address is the memory location
labels = {}

# each element of this list is one line of assembly code
input_code = []

# each element of this list is one line of binary
output = []

# the line at which first instruction starts (0 indexed)
first_instruction = -1

# total number of lines (0 indexed)
number_of_lines = -1

# =========================================================================
# ===========================GENERAL FUCNTIONS=============================


def input_test():
    # get input from stdin
    instructions_started = False

    for inp in sys.stdin:
        if (not instructions_started) and inp.split(" ")[0] != "var":
            instructions_started = True
            first_instruction = len(input_code)
        input_code.append(inp)

    number_of_lines = len(input_code) - 1


def output_binary():
    # output binary to stdout
    for line in output:
        print(line + "\n")


def iteration1():
    # first iteration error handling
    for line in input_code:

        # check the following errors:
        #     g. Variables not declared at the beginning (1)
        #     h. Missing hlt instruction (1)
        #     i. hlt not being used as the last instruction (1)

        # store variables
        # store labels

        pass
    pass


def iteration2():
    #     a. Typos in instruction name or register name (1 -> 2)
    for line in input_code:
        # send to type specific instruction and append to output if binary
        # if error then clean output, append error and return
        pass
    pass


# =========================================================================
# ======================TYPE SPECIFIC INSTRUCTIONS=========================

# Errors to be handled here:
#     (Use of undefined labels -> type specific)    
#     b. Use of undefined variables (1 -> type specific)
#     d. Illegal use of FLAGS register (1 -> type specific)
#     e. Illegal Immediate values (less than 0 or more than 255) (check in type B instructions)
#     f. Misuse of labels as variables or vice-versa (type-specific check)
#     j. Wrong syntax used for instructions (For example, add instruction being used as a
#         type B instruction ) (type-specific check)

# @RETURN:
#     Return either an error or the binary for that line of code

def type_A(line):
    # if error return error
    # else return binary
    pass
    
def type_B(line):
    # if error return error
    # else return binary
    pass
    
def type_C(line):
    # if error return error
    # else return binary
    pass
    
def type_D(line):
    # if error return error
    # else return binary
    pass
    
def type_E(line):
    # if error return error
    # else return binary
    pass
    
def type_F(line):
    # if error return error
    # else return binary
    pass
    

# =========================================================================
# =================================MAIN====================================


def main():
    input_test()
    iteration1()
    iteration2()
    output_binary()


if __name__ == "__main__":
    main()
