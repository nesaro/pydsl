#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Python  hierarchy class to dot"""

def function(inputdic, inputgt, outputgt):
    if inputdic["input"].string == "": 
        return {}
    filename = inputdic["input"]
    knownclass = {} #{"Name":[childlist]}
    import re
    with open(filename, encoding='utf-8') as f:
        for line in f:
            match = re.match("^class (\w+)(\(.+\))?:", line)
            if match:
                if match.lastindex == 1:
                    knownclass[match.group(1)] = None
                else:
                    knownclass[match.group(1)] = match.group(2)[1:-1].split(",")
    #print(knownclass)
    output = "digraph graphname \n{ "
    for key in knownclass:
        if knownclass[key] is None:
            output += '"' + key + '"\n'
        else:
            for child in knownclass[key]:
                output += '"' + key + '" -> "' + child + "\"\n"
    output += "}"
    return {"output":output}


iclass = "PythonTransformer"
inputdic = {"input":"unixPathGrammar"}
outputdic = {"output":"cstring"}

