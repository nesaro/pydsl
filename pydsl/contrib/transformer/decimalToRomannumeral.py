#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) Mark Pilgrim

#Example from dive into python book
#Under GNU Free Documentation License

_romanNumeralMap = (('M',  1000),
                   ('CM', 900),
                   ('D',  500),
                   ('CD', 400),
                   ('C',  100),
                   ('XC', 90),
                   ('L',  50),
                   ('XL', 40),
                   ('X',  10),
                   ('IX', 9),
                   ('V',  5),
                   ('IV', 4),
                   ('I',  1))


def function(inputdic, inputgt, outputgt):
    output = ""
    result = ""
    if str(inputdic["input"]) != "": 
        value = int(str(inputdic["input"]))
        if value > 4000 or value < 1:
            output = "MMMM"
        else:
            for numeral, integer in _romanNumeralMap:
                while value >= integer:
                    result += numeral
                    value -= integer
            output = result
    return {"output":output}

iclass = "PythonTransformer"
inputdic = {"input":"integer"}
outputdic = {"output":"romanNumerals"}

