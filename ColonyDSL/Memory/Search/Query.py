#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.

"""
Search Queries
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from ColonyDSL.Query import Query, QueryEquality, QueryElement, QueryInclusion, QueryGreaterThan

def str_to_memoryquery(string:str, escape = '\\') -> Query:
    """String a query"""
    #We parse de string and generate an equivalent list
    elementlist = [] 
    pos = 0
    currentword = ""
    while pos < len(string):
        if string[pos] == "&" and string[pos+1] == "&":
            elementlist.append(currentword)
            currentword = ""
            elementlist.append("&&")
            pos += 2
            continue
        elif string[pos] == "|" and string[pos+1] == "|":
            elementlist.append(currentword)
            currentword = ""
            elementlist.append("||")
            pos += 2
            continue
        elif string[pos] == "!":
            elementlist.append(currentword)
            currentword = ""
            elementlist.append("!")
            pos += 1
            continue
        elif string[pos] == "=":
            elementlist.append(currentword)
            currentword = ""
            elementlist.append("=")
            pos += 1
            continue
        elif string[pos] == "@":
            elementlist.append(currentword)
            currentword = ""
            elementlist.append("@")
            pos += 1
            continue
        elif string[pos] == ">":
            elementlist.append(currentword)
            currentword = ""
            elementlist.append(">")
            pos += 1
            continue
        elif string[pos] == escape: #insert next symbol into currentword
            currentword += string[pos] + string[pos+1]
            pos += 2
            continue
        else:
            currentword += string[pos]
            pos += 1
    elementlist.append(currentword)
    if len(elementlist) == 1: #Only one str received
        from ColonyDSL.GlobalConfig import GLOBALCONFIG
        likestr = "/.*" + string + ".*/"
        return Query(QueryEquality("identifier",string))
    else:
        return Query(recursive_str_to_query(string))

def recursive_str_to_query(query_list:list) -> QueryElement:
    from ColonyDSL.Query import AndQueryOperator, OrQueryOperator, NotQueryOperator
    if "||" in query_list:
        index = query_list.index("||")
        term1 = recursive_str_to_query(query_list[:index])
        term2 = recursive_str_to_query(query_list[index+1:])
        return OrQueryOperator(term1, term2)
    if "&&" in query_list:
        index = query_list.index("&&")
        term1 = recursive_str_to_query(query_list[:index])
        term2 = recursive_str_to_query(query_list[index+2:])
        return AndQueryOperator(term1, term2)
    if "!" in query_list:
        index = query_list.index("!")
        term = recursive_str_to_query(query_list[index+2:])
        return NotQueryOperator(term)
    pair = None
    if query_list.count("=") == 1:
        pair = query_list.split("=")
        return QueryEquality(pair[0],pair[1])
    elif query_list.count("@") == 1:
        pair = query_list.split("@")
        return QueryInclusion(pair[0],pair[1])
    elif query_list.count(">") == 1:
        pair = query_list.split(">")
        return QueryGreaterThan(pair[0],pair[1])
    else:
        raise Exception
