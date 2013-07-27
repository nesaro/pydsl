#!/usr/bin/env python2.3
"Identify sequence of a-, b-, c- words"
#
#-- The grammar
def d_phrase(t, s):
    'phrase : words ( ABC | AB | A ) words'
    print "Head:", ''.join(s[0])
    print t[1][0]+":", ''.join(s[1])
    print "Tail:", ''.join(s[2])
def d_words(t):
    'words : word*'
def d_word(t):
    'word : "[a-z]+" '
def d_A(t):
    '''A : "a[a-z]*" '''
    return 'A'
def d_AB(t):
    '''AB : A "b[a-z]*" '''
    return 'AB'
def d_ABC(t):
    '''ABC : AB "c[a-z]*" '''
    return 'ABC'
#
#-- Parse STDIN
from dparser import Parser
from sys import argv, stdin
phrase, arg = stdin.read(), argv[-1]
Parser().parse(phrase, print_debug_info=(arg=='--debug'))
