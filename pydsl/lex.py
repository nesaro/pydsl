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
from networkx.exception import NetworkXError
from itertools import chain
import logging

LOG = logging.getLogger(__name__)


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
    if not isinstance(alphabet, (frozenset, Choice)):
        raise TypeError(alphabet.__class__.__name__)
    if not isinstance(base, frozenset):
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
        elif isinstance(current_alphabet, (frozenset, Choice)):
            for element in current_alphabet:
                if element in base:
                    result.add_edge(current_alphabet, base)
                else:
                    result.add_edge(current_alphabet, element)
                    pending_stack.add(element)
        elif current_alphabet.alphabet:
            result.add_edge(current_alphabet, current_alphabet.alphabet)
            pending_stack.add(current_alphabet.alphabet)
    print_graph(result)
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
        if not isinstance(alphabet, (frozenset, Choice)):
            raise TypeError(alphabet.__class__.__name__)
        if not alphabet:
            raise ValueError
        if not base:
            raise ValueError
        self.target_alphabet = alphabet
        self.base = base


    def __call__(self, data):
        if isinstance(data, str):
            data = [Token(x, ascii_encoding) for x in data]
        from pydsl.token import append_position_to_token_list
        data = append_position_to_token_list(data)

        if not all(isinstance(x, Token) for x in data):
            raise TypeError
        for element in data:
            print("CHECKING data for lexer {}".format(data))
            from pydsl.check import check
            if not check(self.base, [element]):
                raise ValueError('Unexpected input %s for alphabet %s' % (element, self.base))
        if self.base == self.target_alphabet:
            return data
        graph = graph_from_alphabet(self.target_alphabet, self.base)
        print("graph {}".format(graph))
        solved_elements = {}
        print("data {}".format(data))
        graph.node[self.base]['parsed'] = data #Attach data to every element in the graph
        print("base {}".format(self.base))
        digraph_walker_backwards(graph, self.base, populate_element_node)
        #print_graph(graph)
        result = []
        print("SADSADSA")
        print("SADSADSA")
        print("SADSADSA")
        print("SADSADSA")
        print("SADSADSA")
        def visit_graph_inorder(node):
            try:
                predecessors = graph.predecessors(node)
            except NetworkXError:
                pass
            else:
                for child in predecessors:
                    print("CHILD {}".format(child))
                    yield from visit_graph_inorder(child)
            try:
                print("CURRENT {}".format(node))
                tokens = graph.node[node]['parsed']
                print("tokens {}".format(tokens and tokens[0].gd))
                if tokens and tokens[0].gd in self.target_alphabet:
                    yield tokens
            except KeyError:
                pass

        result = list(chain.from_iterable(x for x in visit_graph_inorder(self.base)))
        raise Exception(result)
            


        #for output_alphabet in self.target_alphabet:
        #    print("output_alphabet {}, parsed: {}".format(output_alphabet, graph.node[output_alphabet]['parsed']))
        #    if output_alphabet not in graph.node or 'parsed' not in graph.node[output_alphabet]:
        #        raise Exception("alphabet not initialized:%s" % output_alphabet)
        #    node_results = graph.node[output_alphabet]['parsed']
        #    for token in node_results:
        #        print("after TOKEN: {}".format(token))
        #        #This step needs to flat the token so it matches the signature of the function (base -> alphabet)
        #        result.append(PositionToken(token.content_as_string, output_alphabet, token.left, token.right))
        #result = remove_subsets(result)
        #result = remove_duplicates(result)
        #result = sorted(result, key=lambda x: x.left)
        print(str(x.content) for x in result)

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

def populate_element_node(graph, element):
    gne = graph.node[element]
    if 'parsed' in gne:
        return  # Already parsed
    flat_list = []
    print("CALLBACK element: {}".format(element))
    for successor in graph.successors(element):
        print("CALLBACK successor: {}".format(successor))
        if successor not in graph.node or 'parsed' not in graph.node[successor]:
            raise Exception("Uninitialized graph %s" % successor)
        for pt in graph.node[successor]['parsed']:
            print(("OUTPUT", pt.content, pt.gd, pt.left, pt.right))
            flat_list.append(pt) #This is the alternative point to consolidate

    sorted_flat_list = sorted(flat_list, key=lambda x: x.left) #Orders elements from all sucessors
    print("CALLBACK sorted_flat_list before removing subsets: {}".format(sorted_flat_list))
    sorted_flat_list = remove_subsets(sorted_flat_list)
    print("CALLBACK sorted_flat_list: {}".format(sorted_flat_list))
    lexed_list = []
    prev_right = 0
    for pt in sorted_flat_list:
        #if prev_right != left:
        #    LOG.error("Non contiguous parsing from sucessors {} , current: {}".format(sorted_flat_list, element))
        #    gne['parsed'] = []
        #    return
        #prev_right = right
        lexed_list.append(Token(pt.content, pt.gd))
    from pydsl.extract import extract
    result = extract(element, lexed_list)
    for x in result:
        x.gd = element
    print("CALLBACK element: {} lexed_list {}: extract:{}".format(element, lexed_list, result))
    gne['parsed'] = result #QUESTION : are the positions on the current element indexes or the higher level indexes. In other words, is a join needed?



def digraph_walker_backwards(graph, element, call_back):
    """Visits every element guaranteeing that the previous elements have been visited before"""
    print("digraph_walker_backwards {}".format(element))
    call_back(graph, element)
    for predecessor in graph.predecessors(element):
        print("predecessor {}".format(predecessor))
        call_back(graph, predecessor)
    for predecessor in graph.predecessors(element):
        digraph_walker_backwards(graph, predecessor, call_back)
        print("predecessor 2nd pass {}, {}".format(predecessor, graph.node[predecessor]['parsed']))



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
        for gd in self.alphabet:
            checker = checker_factory(gd)
            left = self.index
            for right in range(left +1, len(self.string) +1):
                if checker.check(self.string[left:right]): #TODO: Use match
                    if right > best_right:
                        best_right = right
                        best_gd = gd
        if not best_gd:
            raise Exception("Nothing consumed")
        result = self.string[self.index:best_right], best_gd
        self.index = right
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
                for right in range(left +1, len(self.string) +1 ):
                    if checker.check(self.string[left:right]):
                        valid_alternatives.append((left, right, gd))
        if not valid_alternatives:
            raise Exception("Nothing consumed")
        for left, right, gd in valid_alternatives:
            string = self.string[left:right]
            tree.append(left, right, string, gd, check_position=False)

        right_length_seq = []
        for x in tree.valid_sequences():
            if x[-1]['right'] == len(self.string):
                right_length_seq.append(x)
        if not right_length_seq:
            raise Exception("No sequence found for input %s alphabet %s" % (self.string,self.alphabet))
        for y in sorted(right_length_seq, key=lambda x:len(x))[0]: #Always gets the match with less tokens
            yield Token(y['content'], y.get('gd'))

def lexer_factory(alphabet, base):
    if alphabet == ascii_encoding:
        return ChoiceBruteForceLexer(alphabet)
    if isinstance(alphabet, Choice) and alphabet.alphabet == base:
        return ChoiceBruteForceLexer(alphabet)
    return GeneralLexer(alphabet, base)

def lex(alphabet, base, data):
    return lexer_factory(alphabet, base)(data)
