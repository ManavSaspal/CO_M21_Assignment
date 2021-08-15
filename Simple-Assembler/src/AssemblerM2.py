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

# the line at which first instruction starts (0 indexed) (empty lines included)
first_instruction = -1

# total number of lines (0 indexed) (empty lines included)
number_of_lines = -1

# the line at which first instruction starts (0 indexed) (empty lines NOT included)
first_instruction_non_empty = -1

# total number of lines (0 indexed) (empty lines NOT included)
number_of_lines_non_empty = -1


# =========================================================================
# ===========================GENERAL FUCNTIONS=============================


def input_test():
    # get input from stdin
    instructions_started = False
    global first_instruction
    global number_of_lines
    global first_instruction_non_empty
    global number_of_lines_non_empty
    for inp in sys.stdin:
        thisline = ""

        for char in inp:
            if char == "\n":
                break
            thisline += char

        if not thisline.split():
            input_code.append("")
            continue

        if (not instructions_started) and thisline.split(" ")[0] != "var":
            instructions_started = True
            first_instruction = len(input_code)
        input_code.append(thisline)

    number_of_lines = len(input_code) - 1

    # for non empty lines
    for line in input_code:
        if line.split():
            number_of_lines_non_empty += 1

    idx = 0
    for line in input_code:
        if line.split():
            if line.split()[0] != "var":
                first_instruction_non_empty = idx
                break
            idx += 1

    # for debugging
    # print(first_instruction)
    # print(number_of_lines)
    # print(first_instruction_non_empty)
    # print(number_of_lines_non_empty)
    # print(input_code)


def output_binary():
    # output binary to stdout
    for line in output:
        print(line)


def iteration1():
    # input_code
    # 0 -> first_instruction - 1 = all var declarations
    # first_instruction -> number_of_lines = all instructions

    # first iteration error handling
    count_instructions = -1

    for i in range(number_of_lines + 1):
        line = input_code[i].split()
        if line != []:
            count_instructions += 1
            if i < first_instruction:
                var_address = (
                    number_of_lines_non_empty
                    - first_instruction_non_empty
                    + 1
                    + count_instructions
                )
                if line[1] in variables:
                    output.clear()
                    output.append(
                        "Error in line "
                        + str(i + 1)
                        + ": cannot decalre multiple variables with the same name"
                    )
                    return

                if line[1] in labels:
                    output.clear()
                    output.append(
                        "Error in line "
                        + str(i + 1)
                        + ": cannot decalre variables and labels with the same name"
                    )
                    return

                variables[line[1]] = f"{var_address:08b}"
            else:
                if line[0] == "var":
                    output.clear()
                    output.append(
                        "Error in line "
                        + str(i + 1)
                        + ": Variables not declared at the beginning"
                    )
                    return

                if line[0][-1] == ":":

                    label_address = count_instructions - first_instruction_non_empty

                    if line[0][0:-1] in labels:
                        output.clear()
                        output.append(
                            "Error in line "
                            + str(i + 1)
                            + ": cannot decalre multiple labels with the same name"
                        )
                        return

                    if line[0][0:-1] in variables:
                        output.clear()
                        output.append(
                            "Error in line "
                            + str(i + 1)
                            + ": cannot decalre labels with the same name as a variable"
                        )
                        return

                    labels[line[0][0:-1]] = f"{label_address:08b}"

                    if (
                        line[1] == "hlt"
                        and count_instructions != number_of_lines_non_empty
                    ):
                        output.clear()
                        output.append(
                            "Error in line "
                            + str(i + 1)
                            + ": hlt not being used as the last instruction"
                        )
                        return

                    if (
                        count_instructions == number_of_lines_non_empty
                        and line[1] != "hlt"
                    ):
                        output.clear()
                        output.append(
                            "Error in line " + str(i + 1) + ": Missing hlt instruction"
                        )
                        return

                else:
                    if line[0] == "hlt":
                        if count_instructions != number_of_lines_non_empty:
                            output.clear()
                            output.append(
                                "Error in line "
                                + str(i + 1)
                                + ": hlt not being used as the last instruction"
                            )
                        return
                    if (
                        count_instructions == number_of_lines_non_empty
                        and line[0] != "hlt"
                    ):

                        output.clear()
                        output.append(
                            "Error in line " + str(i + 1) + ": Missing hlt instruction"
                        )

                        return

    # check the following errors:
    #     g_Variables not declared at the beginning (1)
    #     h_Missing hlt instruction (1)
    #     i_hlt not being used as the last instruction (1)

    # _store variables
    # _store labels


def iteration2():
    # Typos in instruction name or register name (1 -> 2)
    # send to type specific instruction and append to output if binary
    # if error then clean output, append error and return

    for i in range(first_instruction, number_of_lines + 1):
        if not input_code[i]:
            continue

        if input_code[i].split()[0][-1] == ":":
            newline = ""

            for t in range(1, len(input_code[i].split())):

                newline += " " + input_code[i].split()[t]
            input_code[i] = newline

        instruction = input_code[i].split()[0]
        binary_output = []

        if instruction not in bin_encoding.typecodes:

            output.clear()
            if instruction == "var":
                output.append(
                    "Error in line "
                    + str(i + 1)
                    + ": Cannot declare variables after labels, expected an instruction"
                )
            else:
                output.append(
                    "Error in line "
                    + str(i + 1)
                    + ": There doesn't exist any instruction with name "
                    + instruction
                )
            return

        if instruction == "mov":
            if len(input_code[i].split()) < 3:
                output.clear()
                output.append(
                    "Error in line "
                    + str(i + 1)
                    + " invalid syntax for mov instruction"
                )
                return

            if input_code[i].split()[2][0] == "$":
                binary_output = type_B(input_code[i])
            else:
                binary_output = type_C(input_code[i])

        elif bin_encoding.typecodes[instruction] == "A":

            binary_output = type_A(input_code[i])

        elif bin_encoding.typecodes[instruction] == "B":

            binary_output = type_B(input_code[i])

        elif bin_encoding.typecodes[instruction] == "C":

            binary_output = type_C(input_code[i])

        elif bin_encoding.typecodes[instruction] == "D":

            binary_output = type_D(input_code[i])

        elif bin_encoding.typecodes[instruction] == "E":
            binary_output = type_E(input_code[i])

        elif bin_encoding.typecodes[instruction] == "F":
            binary_output = type_F(input_code[i])

        if not binary_output:
            print("UNHANDLED ERROR AT ITERATION 2")
        elif binary_output[0]:
            output.append(binary_output[1])
        else:
            output.clear()
            output.append("Error in line " + str(i + 1) + " " + binary_output[1])
            return


# comment
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


def tobinary(n):
    return bin(n).replace("0b", "")


def valid_reg(reg):
    # return true if value of reg is valid and reg!=flag
    if reg in bin_encoding.registorcodes and reg != "FLAGS":
        return True
    return False


def error_registor(reg):
    # returns (False,error statement for registor)
    if reg == "FLAGS":
        return (False, "illegal use of  FLAGS registor")
    return (False, "invalid registor" + reg)


def type_A(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if len(inp) != 4:
        return (False, "wrong syntax used for type A instruction")
    ans = bin_encoding.opcodes[inp[0]]
    r = []
    for i in range(3):
        if valid_reg(inp[i + 1]):
            r.append(bin_encoding.registorcodes[inp[i + 1]])
        else:
            return error_registor(inp[i + 1])
    return (True, ans + "00" + r[0] + r[1] + r[2])


def type_B(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if len(inp) != 3:
        return (False, "wrong syntax used for type B instruction")
    ans = bin_encoding.opcodes[inp[0]]
    x = []
    if inp[0] == "mov":
        ans = "00010"
    if valid_reg(inp[1]):
        ans += bin_encoding.registorcodes[inp[1]]
    else:
        return error_registor(inp[1])
    inp[2] = inp[2][1:]
    imm = int(inp[2])
    if imm < 0 or imm > 255:
        return (False, "Illegal Immediate value " + str(imm))
    else:
        imm = tobinary(imm)
        z = 8 - len(imm)
        ans += "0" * z + imm

    return (True, ans)


def type_C(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if len(inp) != 3:
        return (False, "wrong syntax used for type C instruction")
    ans = bin_encoding.opcodes[inp[0]]
    if inp[0] == "mov":
        ans = "00011" + "0" * 5
        if valid_reg(inp[1]):
            ans += bin_encoding.registorcodes[inp[1]]
            if inp[2] in bin_encoding.registorcodes:
                ans += bin_encoding.registorcodes[inp[2]]
            else:
                return error_registor(inp[2])
        else:
            return error_registor(inp[1])
        return (True, ans)
    ans += "0" * 5
    for i in range(2):
        if valid_reg(inp[i + 1]):
            ans += bin_encoding.registorcodes[inp[i + 1]]
        else:
            return error_registor(inp[i + 1])

    return (True, ans)


def type_D(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if len(inp) != 3:
        return (False, "wrong syntax used for type D instruction")
    ans = bin_encoding.opcodes[inp[0]]

    if valid_reg(inp[1]):
        ans += bin_encoding.registorcodes[inp[1]]

    else:
        return error_registor(inp[1])

    if inp[2] in variables:

        ans += variables[inp[2]]
    else:
        if inp[2] in labels:
            return (False, "misuse of label " + inp[2] + " as variable")

        return (False, "undefined variable " + inp[2])

    return (True, ans)


def type_E(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if len(inp) != 2:
        return (False, "wrong syntax used for type E instruction")

    ans = bin_encoding.opcodes[inp[0]] + "0" * 3
    if inp[1] in labels:
        ans += labels[inp[1]]

    else:
        if inp[1] in variables:
            return (False, "misuse of variable " + inp[1] + " as label")
        return (False, "undefined label  " + inp[1])

    return (True, ans)


def type_F(line):
    # if error return (False,error statement)
    inp = line.split()
    if len(inp) != 1:
        return (False, "wrong syntax used for type F instruction")
    return (True, "10011" + "0" * 11)


# =========================================================================
# =================================MAIN====================================


def main():
    input_test()

    iteration1()
    # print(variables)
    if len(output) == 0:
        iteration2()
    output_binary()


if __name__ == "__main__":
    main()
