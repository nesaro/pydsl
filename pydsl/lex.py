#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Lexer classes. Receives and input sequences and returns a list of Tokens"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2017, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.grammar.PEG import Choice
from pydsl.check import checker_factory
from pydsl.token import Token, PositionToken
from pydsl.tree import PositionResultList
from pydsl.encoding import ascii_encoding


class DummyLexer(object):

    """Special Lexer that encodes from a string a reads a string"""

    def __call__(self, string):
        for x in string:
            yield Token(x, ascii_encoding)


#A1 A2
#|  |
#A3 A4
#|  |
#A5 |
#\  /
# A6

#Order is not always unique, as in the previous example A4 could be extracter after or before A3. At the moment the algorithm is to compute elements of the longest path first (extract elements from longest path every single time)


#Check that every element in the input belongs to base

#Call the lexers following the graph


def graph_from_alphabet(alphabet, base):
    """Creates a graph that connects the base with the target through alphabets
    If every target is connected to any inputs, create the independent paths"""
    if not isinstance(alphabet, Choice):
        raise TypeError(alphabet.__class__.__name__)
    if not isinstance(base, Choice):
        raise TypeError(base.__class__.__name__)
            
    import networkx
    result = networkx.DiGraph()
    current_alphabet = alphabet
    pending_stack = set(current_alphabet)
    while pending_stack:
        current_alphabet = pending_stack.pop()
        if current_alphabet == base:
            continue
        if current_alphabet in base:
            result.add_edge(current_alphabet, base)
        elif isinstance(current_alphabet, Choice):
            for element in current_alphabet:
                if element in base:
                    result.add_edge(current_alphabet, base)
                else:
                    result.add_edge(current_alphabet, element)
                    pending_stack.add(element)
        elif current_alphabet.alphabet:
            result.add_edge(current_alphabet, current_alphabet.alphabet)
            pending_stack.add(current_alphabet.alphabet)
    return result

def print_graph(result):
    import networkx
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,8))
    # with nodes colored by degree sized by population
    networkx.draw(result, with_labels=True)
    plt.savefig("knuth_miles.png")

class GeneralLexer(object):
    """Multi level lexer"""
    def __init__(self, alphabet, base):
        if not isinstance(alphabet, Choice):
            raise TypeError(alphabet.__class__.__name__)
        if not alphabet:
            raise ValueError
        if not base:
            raise ValueError
        self.alphabet = alphabet
        self.base = base


    def __call__(self, data):
        if isinstance(data, str):
            data = [Token(x, ascii_encoding) for x in data]
        from pydsl.token import append_position_to_token_list
        data = append_position_to_token_list(data)

        if not all(isinstance(x, Token) for x in data):
            raise TypeError
        for element in data:
            from pydsl.check import check
            if not check(self.base, [element]):
                raise ValueError('Unexpected input %s for alphabet %s' % (element, self.base))
        if self.base == self.alphabet:
            return data
        graph = graph_from_alphabet(self.alphabet, self.base)
        solved_elements = {}
        graph.node[self.base]['parsed'] = data #Attach data to every element in the graph
        #print_graph(graph)
        digraph_walker_backwards(graph, self.base, my_call_back)
        result = []
        for output_alphabet in self.alphabet:
            if output_alphabet in self.base:
                output_alphabet = self.base
            if output_alphabet not in graph.node or 'parsed' not in graph.node[output_alphabet]:
                raise Exception("alphabet not initialized:%s" % output_alphabet)
            for token in graph.node[output_alphabet]['parsed']:
                result.append(PositionToken(str(token), output_alphabet, token.left, token.right))

        result = sorted(result, key=lambda x: x.left)
        result = remove_subsets(result)
        result = remove_duplicates(result)
        return [Token(x.content, x.gd) for x in result]


def is_subset(a, b):
    """Excluding same size"""
    return b.left <= a.left and b.right > a.right or b.left < a.left and b.right >= a.right 

def remove_subsets(ptoken_list):
    result = []
    for ptoken in ptoken_list:
        if not any((is_subset(ptoken, x) for x in ptoken_list)):
            result.append(ptoken)
    return result

def remove_duplicates(ptoken_list):
    result = []
    for x in ptoken_list:
        for y in result:
            if x.content == y.content and x.left == y.left and x.right == y.right: #ignores GD
                break
        else:
            result.append(x)
    return result

def my_call_back(graph, element):
    gne = graph.node[element]
    if 'parsed' in gne:
        return  # Already parsed
    flat_list = []
    for successor in graph.successors(element):
        if successor not in graph.node or 'parsed' not in graph.node[successor]:
            my_call_back(graph, successor)
        for token in graph.node[successor]['parsed']:
            flat_list.append(token)
    sorted_flat_list = remove_subsets(flat_list)
    lexed_list = []
    prev_right = 0
    for token in sorted_flat_list:
        if prev_right != token.left:
            raise Exception("Non contiguous parsing from sucessors")
        prev_right = token.right
        lexed_list.append(token)
    from pydsl.extract import extract
    gne['parsed'] = extract(element, lexed_list)



def digraph_walker_backwards(graph, element, call_back):
    """Visits every element guaranteeing that the previous elements have been visited before"""
    call_back(graph, element)
    for predecessor in graph.predecessors(element):
        call_back(graph, predecessor)
    for predecessor in graph.predecessors(element):
        digraph_walker_backwards(graph, predecessor, call_back)



class ChoiceLexer(object):
    """Lexer receives an Alphabet in the initialization (A1).
    Receives an input that belongs to A1 and generates a list of tokens in a different Alphabet A2
    It is always described with a regular grammar"""

    def __init__(self, alphabet):
        self.load(None)
        self.alphabet = alphabet

    def load(self, string):
        self.string = string
        self.index = 0

    def __call__(self, string):
        """Tokenizes input, generating a list of tokens"""
        self.load(str(string))
        result = []
        while True:
            try:
                result.append(self.nextToken())
            except:
                break
        return result

    def nextToken(self):
        best_right = 0
        best_gd = None
        matches = []
        for gd in self.alphabet:
            checker = checker_factory(gd)
            if checker.check(self.string[self.index:self.index+1]):
                matches.append(gd)
        if not matches:
            raise Exception("Unmatched Token")
        elif len(matches) > 1:
            raise Exception("Too many matches")
        gd = matches[0]
        result = Token(self.string[self.index:self.index+1], gd)
        self.index += 1
        return result


class ChoiceBruteForceLexer(object):
    """Attempts to generate the smallest token sequence by evaluating every accepted sequence"""

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def __call__(self, string):  # -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.string = string
        return [x for x in self.nextToken()]

    def nextToken(self):
        tree = PositionResultList()  # This is the extract algorithm
        valid_alternatives = []
        for gd in self.alphabet:
            checker = checker_factory(gd)
            for left in range(0, len(self.string)):
                if gd.maxsize:
                    max_right = left+1+gd.maxsize
                else:
                    max_right = len(self.string) + 1
                for right in range(left +1, min(max_right, len(self.string) +1)):
                    slice = self.string[left:right]
                    if checker.check(slice):
                        tree.append(left, right, slice, gd, check_position=False)
        if not tree:
            raise Exception("Nothing consumed")

        right_length_seq = []
        valid_sequences = tree.valid_sequences()
        print("VALID {}".format(valid_sequences))
        for x in valid_sequences:
            my_list = list(x)
            print("MYLIST{}".format(my_list))
            if my_list[-1]['right'] == len(self.string):
                right_length_seq.append(my_list)
        if not right_length_seq:
            raise Exception("No sequence found for input %s alphabet %s" % (self.string,self.alphabet))
        for y in sorted(right_length_seq, key=lambda x:len(x))[0]: #Always gets the match with less tokens
            yield Token(y['content'], y.get('gd'))

def lexer_factory(alphabet, base):
    if alphabet == ascii_encoding:
        return ChoiceLexer(alphabet)
    if isinstance(alphabet, Choice) and alphabet.alphabet == base:
        return ChoiceBruteForceLexer(alphabet)
    return GeneralLexer(alphabet, base)

def lex(alphabet, base, data):
    return lexer_factory(alphabet, base)(data)
