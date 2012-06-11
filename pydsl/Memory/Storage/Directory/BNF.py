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


"""BNF format functions"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
import re
from pydsl.Grammar.Parser.Symbol import StringTerminalSymbol, CharTerminalSymbol, WordTerminalSymbol, BoundariesRules, NonTerminalSymbol, NullSymbol
from pydsl.Grammar.Parser.Production import NonTerminalProduction
LOG = logging.getLogger("BNF")

""" Colony Grammar definition file parser """

def __generateCharSymbol(rightside):
    args = rightside.split(",")
    if args[0] != "Char":
        raise TypeError
    return CharTerminalSymbol(args[1])

def __generateStringSymbol(rightside):
    args = rightside.split(",")
    if args[0] != "String":
        raise TypeError
    content = args[1]
    if args[1][0] == "'" and args[1][-1] == "'":
        content = args[1][1:-1]
    return StringTerminalSymbol(content)

def __generateWordSymbol(rightside):
    args = rightside.split(",")
    if args[0] != "Word":
        raise TypeError
    br = BoundariesRules(args[2], int(args[3]))
    return WordTerminalSymbol(args[1], {"grammarname":args[1]}, br)


def read_nonterminal_production(line, symboldict):
    sidesarray = line.split("::=")
    if len(sidesarray) < 2 or len(sidesarray) > 3:
        raise ValueError
    leftside = sidesarray[0].strip()
    #leftside contains at least one NonTerminalSymbol
    #FIXME supports only one symbol
    symboldict[leftside] = NonTerminalSymbol(leftside)
    rightside = sidesarray[1]
    alternatives = [alt.rstrip() for alt in rightside.split("|")]
    result = []
    n = 0
    for alternative in alternatives:
        symbollist = alternative.split()
        symbolinstancelist = []
        for symbol in symbollist:
            symbolinstancelist.append(symboldict[symbol])
        result.append(NonTerminalProduction([symboldict[leftside]], symbolinstancelist))
        n += 1
    return result

def read_terminal_production(line):
    sidesarray = line.split(":=")
    if len(sidesarray) != 2:
        raise ValueError
    leftside = sidesarray[0]
    leftside = leftside.strip()
    symbolnames = leftside.split(" ")
    if len(symbolnames) != 1:
        LOG.error("Error generating terminal rule: " + line + "At left side")
        raise ValueError
    #leftside is symbolname
    rightside = sidesarray[1]
    rightside = rightside.strip()
    #regexp to detect rightside: Char, String, Grammar
    newsymbol = None
    if re.search("^Char", rightside):
        newsymbol = __generateCharSymbol(rightside)
    elif re.search("^String", rightside):
        newsymbol = __generateStringSymbol(rightside)
    elif re.search("^Word", rightside):
        newsymbol = __generateWordSymbol(rightside)
    else:
        raise ValueError
    return (symbolnames[0], newsymbol)


def strlist_to_production_set(linelist):
    nonterminalrulelist = []
    terminalrulelist = []
    rulelist = []
    symboldict = {"Null":NullSymbol()}
    macrodict = {}
    #first read terminalsymbols
    for line in linelist:
        cleanline = re.sub("//.*$", "", line)
        if re.search("::=", cleanline):
            nonterminalrulelist.append(cleanline)
        elif re.search (":=", cleanline):
            symbolname, symbolinstance = read_terminal_production(cleanline)
            symboldict[symbolname] = symbolinstance
            from pydsl.Grammar.Parser.Production import TerminalProduction
            terminalrulelist.append(TerminalProduction(symbolinstance))
        elif re.search ("^#.*$", cleanline):
            pair = cleanline[1:].split("=")
            assert(len(pair)==2)
            macrodict[pair[0]] = pair[1].rstrip()
        elif re.search ("^\s*$", cleanline):
            pass #Empty line
        else:
            LOG.error("Unknown line at bnf input file")
            raise Exception #TODO find proper exception

    #then read nonterminalsymbols
    while len(nonterminalrulelist) > 0:
        linestodrop = []
        for myindex in range(len(nonterminalrulelist)):
            try:
                newrules = read_nonterminal_production(nonterminalrulelist[myindex], symboldict)
                for newrule in newrules:
                    rulelist.append(newrule)
            except KeyError:
                pass
            else:
                linestodrop.append(myindex)
        linestodrop.reverse()
        if len(linestodrop) == 0:
            LOG.error("No rule found: ")
            raise Exception
        for myindex in linestodrop:
            del nonterminalrulelist[myindex]
    from pydsl.Grammar.Parser.Production import BNFGrammar
    for terminal in terminalrulelist:
        rulelist.append(terminal)
    return BNFGrammar(symboldict["S"], rulelist, macrodict)


def bnf_file_to_productionset(filepath):
    """Converts a metalanguage to a ProductionRuleSet"""
    linelist = []
    with open(filepath,'r', encoding='utf-8') as mlfile:
        for line in mlfile:
            linelist.append(line)
    return strlist_to_production_set(linelist)

def str_to_productionset(string):
    """Converts a str into a ProductionRuleSet"""
    return strlist_to_production_set(string.split('\n'))

