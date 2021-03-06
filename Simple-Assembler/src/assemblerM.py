"""
assembler
"""
import sys
import bin_encoding

# =========================================================================
# =============================STORING DATA================================

resistorcodes = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
}

opcodes = {
    "add": "00000",
    "sub": "00001",
    "mov": "00010",  #check overlap
    "mov": "00011",  #check overlap
    "ld": "00100",
    "st": "00101",
    "mul": "00110",
    "div": "00111",
    "rs": "01000",
    "ls": "01001",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
    "not": "01101",
    "cmp": "01110",
    "jmp": "01111",
    "jlt": "10000",
    "jgt": "10001",
    "je": "10010",
    "hlt": "10011"
    }
    
typecodes = {
    "add": "A",
    "sub": "A",
    "mov": "B",  #check overlap
    "mov": "C",  #check overlap
    "ld": "D",
    "st": "D",
    "mul": "A",
    "div": "C",
    "rs": "B",
    "ls": "B",
    "xor": "A",
    "or": "A",
    "and": "A",
    "not": "C",
    "cmp": "C",
    "jmp": "E",
    "jlt": "E",
    "jgt": "E",
    "je": "E",
    "hlt": "F"
}

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
    # input_code
    # 0 -> first_instruction - 1 = all var declarations
    # first_instruction -> number_of_lines = all instructions  

    # first iteration error handling
    
    for i in range(number_of_lines + 1):
        line = input_code[i].split(" ");
        if(i < first_instruction):
            var_address = number_of_lines - first_instruction + 1 + i
            variables[line[1]] = f'{var_address:08b}'
        else:
            if(line[0] == 'var'):
                output.clear()
                output.append(
                    "Error in line"
                    + str(i)
                    + ": Variables not declared at the beginning"
                )
                return
            if(line[0] == 'hlt' and i != number_of_lines):
                output.clear()
                output.append(
                    "Error in line"
                    + str(i)
                    + ": hlt not being used as the last instruction"
                )
                return
            if(i == number_of_lines and line[0] != 'hlt'):
                output.clear()
                output.append(
                    "Error in line"
                    + str(i)
                    + ": Missing hlt instruction"
                )
                return
            if(line[0][-1] == ':'):
                label_address = i - first_instruction
                labels[line[0][0:-1]] = f'{label_address:08b}'

    # check the following errors:
        #     g_Variables not declared at the beginning (1)
        #     h_Missing hlt instruction (1)
        #     i_hlt not being used as the last instruction (1)

        #_store variables
        #_store labels


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

#comment
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
    
def valid_reg(reg) : 
    #return true if value of reg is valid and reg!=flag 
    if(reg in resistorcodes and reg!="FLAGS"):
        return True
    return False 
    
def error_registor(reg):
    #returns (False,error statement for registor)
    if(reg=="FLAGS"):
        return((False,"illegal use of  FLAGS registor"))
    return((False,"invalid registor"+reg))  
    
def type_A(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if(len(inp)!=4):
        return((False,"wrong syntax used for type A instruction"))
    ans=opcodes[inp[0]]
    r=[]
    for i in range (3):        
        if(valid_reg(inp[i+1])):
            r.append(resistorcodes[inp[i+1]])
        else :
            return(error_registor(inp[i+1]))           
    return (True,ans+"00"+r[0]+r[1]+r[2])
 
def type_B(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if(len(inp)!=3):
     return(False,"wrong syntax used for type B instruction")
    ans=opcodes[inp[0]]
    x=[]
    if(inp[0]=="mov"):
        ans="00010"
    if(valid_reg(inp[1])):
        ans+=resistorcodes[inp[1]]
    else:
        return error_registor(inp[1]) 
    inp[2]=inp[2][1:]  
    imm = int(inp[2])
    if(imm<0 or imm > 255):
        return (False,"Illegal Immediate value "+str(imm))
    else:
        imm= tobinary(imm)      
        z=8-len(imm)
        ans+="0"*z+imm
    
            
    return (True,ans)
    
  
def type_C(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if(len(inp)!=3):
        return (False,"wrong syntax used for type C instruction")
    ans=opcodes[inp[0]]
    if(inp[0]=="mov"):
        ans="00011"+"0"*5
        if(valid_reg(inp[1])):
            ans+=(resistorcodes[inp[1]])
            if(inp[2] in resistorcodes):
                ans+=resistorcodes[inp[2]]
            else:
                return error_registor(inp[2])
        else:
            return(error_registor(inp[1])) 
        return (True,ans)     
    ans+="0"*5
    for i in range(2):
        if(valid_reg(inp[i+1])):
            ans+=(resistorcodes[inp[i+1]])
        else :
            return error_registor(inp[i+1])
         
            
    return (True,ans)
      
    
def type_D(line):
   # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if(len(inp)!=3):
     return((False,"wrong syntax used for type D instruction"))
    ans=opcodes[inp[0]]
    
    if(valid_reg(inp[1])):
        ans+=resistorcodes[inp[1]]

    else:
        return error_registor(inp[1]) 
    if(inp[2] in variables):
        ans+=variables[inp[2]]
    else:
        if(inp[2] in labels):
            return(False,"misuse of label "+inp[2]+" as variable")
        return(False,"undefined variable " + inp[2])
            
    return (True,ans)
    
    
def type_E(line):
    # if error return (False,error statement)
    # else return (True ,binary)
    inp = line.split()
    if(len(inp)!=2):
        return(False,"wrong syntax used for type E instruction")

    ans=opcodes[inp[0]] 
    if(inp[1] in labels):
        ans+=labels[inp[1]]
    else:
        if(inp[2] in variables):
            return(False,"misuse of variable "+inp[1]+" as label")
        return (False,"undefined label"+inp[1])

     
            
    return (True,ans)


def type_F(line):
    # if error return (False,error statement)
    inp = line.split()
    if(len(inp)!=1):
        return (False,"wrong syntax used for type F instruction")
    return (True,"10011"  +"0"*11 ) 
    
    
# =========================================================================
# =================================MAIN====================================


def main():
    # input_test()
    iteration1()
    iteration2()
    output_binary()
    print("hello")


if __name__ == "__main__":
    main()
