#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"Tree class for tree based parsers"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from pydsl.Abstract import TypeCheckList
from abc import ABCMeta
LOG = logging.getLogger(__name__)

def nodedist(a, b):
    if a == b:
        return 0
    assert(a.content != b.content) #For testing, but wrong
    return 1

def traversePreOrder(item):
    from pydsl.Abstract import TypeCheckList
    result = TypeCheckList(Tree)
    result.append(item)
    for child in item.childlist:
        result += traversePreOrder(child)
    return result

def traverseInOrder(item):
    result = TypeCheckList(Tree)
    result.append(traverseInOrder(item.childlist[0]))
    result.append(item)
    for childindex in range(1, len(item.childlist)):
        result += traverseInOrder(item.childlist[childindex])
    return result

def traversePostOrder(item):
    result = TypeCheckList(Tree)
    for child in item.childlist:
        result += traversePostOrder(child)
    result.append(item)
    return result

class Tree(metaclass = ABCMeta):
    def __init__(self, leftpos, rightpos, content, valid = True):
        self.leftpos = leftpos
        self.rightpos = rightpos
        self.childlist = TypeCheckList(Tree)
        self.content = content
        self.valid = valid
        
    def __bool__(self):
        """checks if it is a null result"""
        return self.valid

    def __getitem__(self, key, order = "preorder"): #FIXME: getitem and optional argument??
        result = []
        mylist = self.getAllByOrder(order)
        for element in mylist:
            if element.content == key:
                result.append(element)
        return result

    def getItemByOrder(self, key, order):
        if order == "preorder":
            return traversePreOrder(self)
        elif order == "inorder":
            return traverseInOrder(self)
        elif order == "postorder":
            return traversePostOrder(self)
        else:
            raise KeyError

    def getAllByOrder(self, order = "preorder"):
        if order == "preorder":
            return traversePreOrder(self)
        elif order == "inorder":
            return traverseInOrder(self)
        elif order == "postorder":
            return traversePostOrder(self)
        else:
            raise KeyError

    def shift(self, amount):
        """ shifts position """
        self.leftpos += amount
        self.rightpos += amount

    def append_child(self, dpr):
        """appends dpr to childlist"""
        self.childlist.append(dpr)

    def __len__(self):
        return self.rightpos - self.leftpos

    def coverage(self):
        if not(self):
            return 0, len(self)
        if childlist:
            childtotal = 0
            childcoverage = 0
            for child in childlist:
                newcoverage, newtotal = child.coverage()
                childcoverage += newcoverage
                childtotal += newtotal
            assert(childtotal == len(self))
            return childcoverage, childtotal
        else:
            return len(self), len(self)

    def first_leaf(self):
        """Devuelve la primera hoja a la izq"""
        if self.childlist:
            return self.childlist[0].first_leaf()
        else:
            return self

class AST(Tree):
    """Una representacion más simple de la descomposicion, sin alusion a los pasos intermedios"""
    def __init__(self, content, leftpos:int, rightpos:int, production, parentnode = None, valid = True):
        Tree.__init__(self, leftpos, rightpos, content, valid)
        from pydsl.Abstract import TypeCheckList
        self.production = production 
        self.parentnode = parentnode

    def __eq__(self, other):
        try:
            return self.production == other.production and self.content == other.content and self.leftpos == other.leftpos and self.rightpos == other.rightpos and self.valid == other.valid
        except AttributeError:
            return False

    def parent(self, level = 1):
        if level <= 0:
            return self
        elif self.parentnode == None:
            return None
        else:
            return self.parentnode.parent(level -1)

    def ancestors(self)->list:
        result = []
        node = self.parent()
        while node != None:
            result.append(node)
            node = node.parent()
        return result

    def append_child(self, child):
        """appends dpr to childlist"""
        child.parentnode = self
        self.childlist.append(child)

    def __getitem__(self, index):
        result = []
        if self.production.leftside[0].name == index:
            result.append((self.leftpos, self.rightpos))
        else:
            LOG.debug("Not equal: " + str(self.production.leftside[0].name) + " and :" + str(index))
        for child in self.childlist:
            result += child.__getitem__(index)
        return result


    def __contains__(self, index):
        if not self.production.leftside:
            return False
        if self.production.leftside[0].name == index:
            return True
        for child in self.childlist:
            if index in child:
                return True
        return False


class ParseTree(Tree):
    """ Stores a descent parser iteration result """
    def __init__(self, leftpos, rightpos, symbollist:list, content, production, childlist:list = [], valid:bool = True):
        if not isinstance(leftpos, int) and leftpos != None:
            raise TypeError
        if not isinstance(rightpos, int) and rightpos != None:
            raise TypeError
        from .BNF import Production
        if production != None and not isinstance(production, Production):
            print(production)
            raise TypeError
        Tree.__init__(self, leftpos, rightpos, content, valid)
        self.symbollist = symbollist
        self.production = production
        if not childlist:
            childlist = TypeCheckList(ParseTree)
        else:
            childlist = TypeCheckList(ParseTree, childlist)
        self.childlist = childlist #This list stores rule's rightside DescentParserResults 

    def __str__(self):
        result = "<ParseTree: " 
        result += "(" + str(self.leftpos) + "," + str(self.rightpos) 
        result += ") SymbolList: " 
        if len(self.symbollist) == 1:
            result += str(self.symbollist[0])
        else:
            result += str(self.symbollist) 
        result += " Information: " + str(self.content)
        if self.childlist:
            result += ", children: " + str(self.childlist)
        result += " >"
        return result

    def __add__(self, other):
        """ Adds two results. Only if self.rightpos = other.leftpos and parents are the same """
        if not isinstance(other, ParseTree):
            raise TypeError
        if other == []:
            return ParseTree(self.leftpos, self.rightpos, self.symbollist, self.content, self.production, self.childlist) #FIXME: Debe devolver copia de childlist
        if self.rightpos == other.leftpos and self.production == other.production:
            leftpos = self.leftpos
            rightpos = other.rightpos
            production = self.production
            content = self.content + other.content
            symbollist = self.symbollist + other.symbollist
            childlist = self.childlist + other.childlist
            return ParseTree(leftpos, rightpos, symbollist, content, production, childlist)
        else:
            LOG.warning("Unable to add parser results")
            raise Exception

    def split(self):
        """splits a result"""
        result = TypeCheckList(ParseTree)
        for symbol in self.symbollist:
            currentlist = self.childlist
            while len(currentlist) > 1 and len(currentlist[0].symbollist) > 1 and currentlist[0].symbollist[0] != symbol:
                for dpr in currentlist:
                    if symbol in dpr.symbollist:
                        currentlist = dpr.childlist
                        break
                break #Not found
            assert(len(currentlist < 2))
            dpr = currentlist[0]
            currentsymbol = dpr.symbollist[0]
            if len(dpr.symbollist) > 0:
                pass
                #Ir eliminando los simbolos de alrededor hasta que se quede solo el que nos interesa junto a su word
            if currentsymbol != symbol:
                #Not found
                raise Exception
            result.append(dpr)
        return result
    

def parser_to_post_tree(pan:ParseTree, parent = None) -> AST:
    """Converts a parser temporal node into a postnode"""
    result = AST(pan.content, pan.leftpos, pan.rightpos, pan.production, parent, pan.valid)
    for child in pan.childlist:
        childnode = parser_to_post_tree(child, result)
        result.append_child(childnode)
    return result


#Original implementation: https://github.com/irskep/zhang-shasha and https://github.com/timtadh/zhang-shasha

def zss_distance(tree1, tree2):
    treedists = {}
    o1 = tree1.getAllByOrder("postorder")
    o2 = tree2.getAllByOrder("postorder")
    LOG.debug([x.content for x in o1])
    LOG.debug([x.content for x in o2])
    l1 = [o1.index(x.first_leaf()) for x in o1]
    l2 = [o2.index(x.first_leaf()) for x in o2]

    def treedist(i, j):
        if i in treedists and j in treedists[i]: 
            return treedists[i][j] #Cached!
        def s(i, j, v):
            if i not in treedists: 
                treedists[i] = {} 
            treedists[i][j] = v
        forestdists = {}
        def gfd(a:tuple, b:tuple): # get an item from the forest dists dict
            if (a,b) in forestdists:
                return forestdists[(a,b)]
            if a[0] >= a[1] and b[0] >= b[1]: # δ(θ, θ) = 0
                return 0
            if b[0] >= b[1]:
                return forestdists[(a,(0,0))]
            if a[0] >= a[1]:
                return forestdists[((0,0),b)]

        for x in range(l1[i], i+1):
            forestdists[(l1[i], x), (0,0)] = gfd((l1[i],x-1),(0,0)) + 1

        for y in range(l2[j], j+1):
            forestdists[(0,0),(l2[j], y)] = gfd((0,0),(l2[j],y-1)) + 1

        for x in range(l1[i], i+1):
            for y in range(l2[j], j+1):
                if (l1[i] == l1[x] and l2[j] == l2[y]):
                    #Inside the same keyroot
                    forestdists[((l1[i],x),(l2[j],y))] = min(
                            (gfd((l1[i],x-1),(l2[j],y)) + 1),
                            (gfd((l1[i],x),(l2[j],y-1)) + 1),
                            (gfd((l1[i],x-1),(l2[j],y-1)) + nodedist(o1[x], o2[y])))
                    s(x,y, forestdists[((l1[i],x),(l2[j],y))])
                else:
                    forestdists[((l1[i],x),(l2[j],y))] = min(
                            (gfd((l1[i],x-1),(l2[j],y)) + 1),
                            (gfd((l1[i],x),(l2[j],y-1)) + 1),
                            (gfd((l1[i],l1[x]-1),(l2[j],l2[y]-1)) + treedist(x,y)))

        return treedists[i][j]

    keyroots1 = {}
    keyroots2 = {}
    for i in range(len(o1)):
        keyroots1[l1[i]] = i
    for j in range(len(o2)):
        keyroots2[l2[j]] = j
    keyroots1 = sorted(keyroots1.values())
    keyroots2 = sorted(keyroots2.values())
    for x in keyroots1:
        for y in keyroots2:
            result = treedist(x, y)
            #print(x,y,result)
    return result
    




