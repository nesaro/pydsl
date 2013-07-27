#!/usr/bin/env python

import math
import operator
import string
import tpg

if tpg.__python__ == 3:
    operator.div = operator.truediv
    raw_input = input

def make_op(op):
    return {
        '+'   : operator.add,
        '-'   : operator.sub,
        '*'   : operator.mul,
        '/'   : operator.div,
        '%'   : operator.mod,
        '^'   : lambda x,y:x**y,
        '**'  : lambda x,y:x**y,
        'cos' : math.cos,
        'sin' : math.sin,
        'tan' : math.tan,
        'acos': math.acos,
        'asin': math.asin,
        'atan': math.atan,
        'sqr' : lambda x:x*x,
        'sqrt': math.sqrt,
        'abs' : abs,
        'norm': lambda x,y:math.sqrt(x*x+y*y),
    }[op]

class Calc(tpg.Parser, dict):
    r"""
        separator space '\s+' ;

        token pow_op    '\^|\*\*'                                               $ make_op
        token add_op    '[+-]'                                                  $ make_op
        token mul_op    '[*/%]'                                                 $ make_op
        token funct1    '(cos|sin|tan|acos|asin|atan|sqr|sqrt|abs)\b'           $ make_op
        token funct2    '(norm)\b'                                              $ make_op
        token real      '(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+'    $ float
        token integer   '\d+'                                                   $ int
        token VarId     '[a-zA-Z_]\w*'                                          ;

        START/e ->
                'vars'                  $ e=self.mem()
            |   VarId/v '=' Expr/e      $ self[v]=e
            |   Expr/e
        ;

        Var/$self.get(v,0)$ -> VarId/v ;

        Expr/e -> Term/e ( add_op/op Term/t     $ e=op(e,t)
                         )*
        ;

        Term/t -> Fact/t ( mul_op/op Fact/f     $ t=op(t,f)
                         )*
        ;

        Fact/f ->
                add_op/op Fact/f                $ f=op(0,f)
            |   Pow/f
        ;

        Pow/f -> Atom/f ( pow_op/op Fact/e      $ f=op(f,e)
                        )?
        ;

        Atom/a ->
                real/a
            |   integer/a
            |   Function/a
            |   Var/a
            |   '\(' Expr/a '\)'
        ;

        Function/y ->
                funct1/f '\(' Expr/x '\)'               $ y = f(x)
            |   funct2/f '\(' Expr/x1 ',' Expr/x2 '\)'  $ y = f(x1,x2)
        ;

    """

    def mem(self):
        vars = sorted(self.items())
        memory = [ "%s = %s"%(var, val) for (var, val) in vars ]
        return "\n\t" + "\n\t".join(memory)

print("Calc (TPG example)")
calc = Calc()
while 1:
    l = raw_input("\n:")
    if l:
        try:
            print(calc(l))
        except Exception:
            print(tpg.exc())
    else:
        break
