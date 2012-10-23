#!/usr/bin/python
# -*- coding: utf-8 -*-

def function(inputdic, inputgt, outputgt):
    mainstr =  inputdic['input']
    pointer = 0
    memory = {}
    index = 0
    result = ""
    while index in range(len(mainstr)):
        x = mainstr[index]
        if x == '>':
            pointer += 1
            index += 1
        elif x == '<':
            pointer -= 1
            index += 1
        elif x == '+':
            if not pointer in memory:
                memory[pointer] = 0
            memory[pointer] += 1
            index += 1
        elif x == '-':
            if not pointer in memory:
                memory[pointer] = 0
            memory[pointer] -= 1
            index += 1
        elif x == '.':
            result += chr(memory[pointer])
            index += 1
        elif x == ',':
            memory[pointer] = ord(result[-1])
            index += 1
        elif x == '[':
            if not memory.get(pointer, 0):
                index += 1
                while mainstr[index] != ']':
                    index+=1
            index += 1
        elif x == ']':
            if memory.get(pointer, 0):
                index -= 1
                while mainstr[index] != '[':
                    index-=1
            index += 1
    return {"output":result}


inputdic = { "input":"brainfuck"}
outputdic = {"output":"cstring"}
iclass = "PythonTransformer"
