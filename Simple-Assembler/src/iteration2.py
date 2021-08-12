"""
    JUST COPY THE "register_error" AND "iteration2" FUNCTIONS TO ASSEMBLER.PY
"""

import bin_encoding


# ======================================================================================
# ======================================================================================
# ======================================================================================
# TEMPORARY CODE FOR TESTING
# NOT TO BE COPIED TO ASSEMBLER.PY

# input_code = ["var x", "hlt", "jgt R2R4R2", "je R2R4R2"]
# output = []
# first_instruction = 1
# number_of_lines = 3


# def type_A(line):
#     # if error return error
#     # else return binary
#     return [True, "type_A"]


# def type_B(line):
#     # if error return error
#     # else return binary
#     return [True, "type_B"]


# def type_C(line):
#     # if error return error
#     # else return binary
#     return [True, "type_C"]


# def type_D(line):
#     # if error return error
#     # else return binary
#     return [True, "type_D"]


# def type_E(line):
#     # if error return error
#     # else return binary
#     return [True, "type_E"]


# def type_F(line):
#     # if error return error
#     # else return binary
#     return [True, "type_F"]

# =======================================================================================
# =======================================================================================
# =======================================================================================

# helper function for iteration2
def register_error(line, line_number, indices):
    line = line.split(" ")
    for i in indices:
        try:
            regname = line[i][0:1]
            regnumber = int(line[i][1:])
        except:
            output.clear()
            output.append(
                "Error in line " + str(line_number + 1) + ": Incorrect register name"
            )
            return True
        else:
            if regname != "R" or regnumber > 6 or regnumber < 0:
                output.clear()
                output.append(
                    "Error in line " + str(line_number + 1) + ": Incorrect register name"
                )
                return True
    return False


def iteration2():
    # Typos in instruction name or register name (1 -> 2)
    # send to type specific instruction and append to output if binary
    # if error then clean output, append error and return

    for i in range(first_instruction, number_of_lines + 1):
        instruction = input_code[i].split(" ")[0]
        binary_output = []

        if instruction not in bin_encoding.typecodes:
            output.clear()
            output.append(
                "Error in line"
                + str(i)
                + ": There doesn't exist any instruction with that name"
            )
            return

        if instruction == "mov":
            if input_code[i].split(" ")[2][0] == "$":
                if register_error(input_code[i], i, [1]):
                    return
                binary_output = type_B(input_code[i])
            else:
                if register_error(input_code[i], i, [1, 2]):
                    return
                binary_output = type_C(input_code[i])

        elif bin_encoding.typecodes[instruction] == "A":
            if register_error(input_code[i], i, [1, 2, 3]):
                return
            binary_output = type_A(input_code[i])

        elif bin_encoding.typecodes[instruction] == "B":
            if register_error(input_code[i], i, [1]):
                return
            binary_output = type_B(input_code[i])

        elif bin_encoding.typecodes[instruction] == "C":
            if register_error(input_code[i], i, [1, 2]):
                return
            binary_output = type_C(input_code[i])

        elif bin_encoding.typecodes[instruction] == "D":
            if register_error(input_code[i], i, [1]):
                return
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
            output.append(binary_output[1])
            return


if __name__ == "__main__":
    iteration2()
    for line in output:
        print(line)
