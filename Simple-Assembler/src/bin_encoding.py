# this is temporary, would need to think if we even need this?

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