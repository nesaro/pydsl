#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Prints a parsetree"""

def symbollist_print(sl):
    resultlist = []
    for element in sl:
        resultlist.append(element.name)
    return ",".join(resultlist)
    

def tree_to_dot(stt):
    output = "digraph graphname \r{ "
    names, relations = aux_stt_dot(stt.first_item)
    for name in names:
        output += '"' + name + '"\r'
    for relation in relations: 
        output += '"' + relation[0] + '" -> "' + relation[1] + "\"\r"
    output += "}"
    return output

def treenode_to_name(treenode):
    result = treenode.word.string
    if len(treenode.rightside) == 1:
        result += " " + str(treenode.rightside[0]) 
    result += " (" + str(treenode.leftpos) + "," + str(treenode.rightpos) + ")"
    return result 

def aux_stt_dot(stt, names = [], relations = []):
    currentname = treenode_to_name(stt)
    if not str(currentname) in names:
        names.append(currentname)
    for child in stt.childlist:
        relations.append((currentname, treenode_to_name(child))) #+ symbollist_print(child.production.rightside)))
        aux_stt_dot(child, names, relations) 
    return(names,relations)
    

def function(inputdic, inputgt, outputgt):
    grammarname =  inputdic['grammar']
    from pydsl.Memory.Loader import load_parser
    grammar = load_parser(grammarname)
    result = grammar.get_trees(inputdic['string'])
    #print(result)
    #print(result[0])
    result = result[0]
    return {"output":tree_to_dot(result)}


inputdic = {"grammar":"cstring", "cstring":"cstring"}
outputdic = {"output":"cstring"}
iclass = "PythonTransformer"
