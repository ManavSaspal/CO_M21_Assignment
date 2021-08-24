# this is temporary, would need to think if we even need this?

opcodes = {
     "00000" : "add",
     "00001" : "sub",
     "00010" : "mov",   #check overlap
     "00011" : "mov",   #check overlap
     "00100" : "ld",
     "00101" : "st",
     "00110" : "mul",
     "00111" : "div",
     "01000" : "rs",
     "01001" : "ls",
     "01010" : "xor",
     "01011" : "or",
     "01100" : "and",
     "01101" : "not",
     "01110" : "cmp",
     "01111" : "jmp",
     "10000" : "jlt",
     "10001" : "jgt",
     "10010" : "je",
     "10011" : "hlt"
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
