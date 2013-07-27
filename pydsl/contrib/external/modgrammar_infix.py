#!/usr/bin/python3

import sys
from modgrammar import *

grammar_whitespace_mode = 'optional'

class Number (Grammar):
    grammar = (OPTIONAL('-'), WORD('0-9'), OPTIONAL('.', WORD('0-9')))

    def value(self):
        return float(self.string)

class ParenExpr (Grammar):
    grammar = (L('('), REF('Expr'), L(')'))

    def value(self):
        return self[1].value()

class P0Term (Grammar):
    grammar = (ParenExpr | Number)

    def value(self):
        return self[0].value()

class P0Expr (Grammar):
    grammar = (P0Term, ONE_OR_MORE(L('/'), P0Term))

    def value(self):
        value = self[0].value()
        for e in self[1]:
            value /= e[1].value()
        return value

class P1Term (Grammar):
    grammar = (P0Expr | ParenExpr | Number)

    def value(self):
        return self[0].value()

class P1Expr (Grammar):
    grammar = (P1Term, ONE_OR_MORE(L('*'), P1Term))

    def value(self):
        value = self[0].value()
        for e in self[1]:
            value *= e[1].value()
        return value

class P2Term (Grammar):
    grammar = (P0Expr | P1Expr | ParenExpr | Number)

    def value(self):
        return self[0].value()

class P2Expr (Grammar):
    grammar = (P2Term, ONE_OR_MORE(L('+') | L('-'), P2Term))

    def value(self):
        value = self[0].value()
        for e in self[1]:
            if e[0].string == '+':
                value += e[1].value()
            else:
                value -= e[1].value()
        return value

class Expr (Grammar):
    grammar = (P2Expr | P1Expr | P0Expr | ParenExpr | Number)

    def value(self):
        return self[0].value()

if __name__ == '__main__':
    parser = Expr.parser()
    result = parser.parse_text(sys.argv[1], eof=True)
    remainder = parser.remainder()
    print("Parsed Text: {}".format(result))
    print("Unparsed Text: {}".format(remainder))
    print("Value: {}".format(result.value()))
