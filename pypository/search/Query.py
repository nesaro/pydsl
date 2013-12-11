#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pypository.
#
#pypository is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pypository is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pypository.  If not, see <http://www.gnu.org/licenses/>.

"""
Search Queries
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class QueryElement(object):
    pass

class QueryTerm(QueryElement):
    """Any query Term"""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __hash__(self):
        return hash(self.left) ^ hash(self.right)


class QueryEquality(QueryTerm):
    """ a = b. It can use a string or a regexp"""
    def __str__(self):
        return "<" + str(self.left) + "=" + str(self.right) + ">"

class QueryPartial(QueryTerm):
    """ a = b. It can use a string or a regexp"""
    def __str__(self):
        return "<" + str(self.left) + "=~" + str(self.right) + ">"

class QueryInclusion(QueryTerm):
    """ looks for an element within a list """
    def __init__(self, left, right, dict_member = "values"):
        """dict_member could be keys or values"""
        QueryTerm.__init__(self, left, right)
        self.dict_member = dict_member

class BinaryOperator(QueryElement):
    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2

class AndQueryOperator(BinaryOperator):
    def __str__(self):
        return "<" + str(self.element1) + "&&" + str(self.element2) + ">"

class OrQueryOperator(BinaryOperator):
    pass

class NotQueryOperator(QueryElement):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return "<!" + str(self.element) + ">"

class Query(object):
    """A generic query"""
    def __init__(self, content):
        self.content = content 

    def qand(self, element):
        self.content = AndQueryOperator(self.content, element)

    def qor(self, element):
        self.content = OrQueryOperator(self.content, element)

    def __str__(self):
        return"<Query:"+str(self.content)+">"


def str_to_memoryquery(string, escape = '\\'):# -> Query:
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
        likestr = "/.*" + string + ".*/"
        return Query(QueryEquality("identifier",string))
    else:
        return Query(recursive_str_to_query(string))

def recursive_str_to_query(query_list): # -> QueryElement:
    if "||" in query_list:
        index = query_list.index("||")
        term1 = recursive_str_to_query(query_list[:index])
        term2 = recursive_str_to_query(query_list[index+2:])
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
    if query_list.count("=") == 1:
        pair = query_list.split("=")
        return QueryEquality(pair[0],pair[1])
    elif query_list.count("@") == 1:
        pair = query_list.split("@")
        return QueryInclusion(pair[0],pair[1])
    else:
        raise Exception

def dict_to_query(querydict): # -> Query:
    return Query(recursive_dict_to_query(querydict))

def recursive_dict_to_query(querydict): # -> QueryElement:
    if isinstance(querydict, str):
        return querydict
    resultlist = []
    for key, value in querydict.items():
        if isinstance(value, dict):
            if len(value) == 1 and "$in" in value:
                resultlist.append(QueryInclusion(key, recursive_dict_to_query(value["$in"])))
            elif len(value) == 1 and "$not" in value:
                resultlist.append(QueryEquality(key,NotQueryOperator(recursive_dict_to_query(value["$not"]))))
            elif len(value) == 1 and "$part" in value:
                resultlist.append(QueryPartial(key, value["$part"]))
            else:
                resultlist.append(recursive_dict_to_query(value))
        elif isinstance(value, str):
            resultlist.append(QueryEquality(key,value))
    myfun = lambda x,y: AndQueryOperator(x,y)
    from functools import reduce
    return reduce(myfun, resultlist)
    

