import lrparsing
from lrparsing import Keyword, List, Prio, Ref, THIS, Token, Tokens

class ExprParser(lrparsing.Grammar):
    #
    # Put Tokens we don't want to re-type in a TokenRegistry.
    #
    class T(lrparsing.TokenRegistry):
        integer = Token(re="[0-9]+")
        integer["key"] = "I a mapping!"
        ident = Token(re="[A-Za-z_][A-Za-z_0-9]*")
    #
    # Grammar rules.
    #
    expr = Ref("expr")                # Forward reference
    call = T.ident + '(' + List(expr, ',') + ')'
    atom = T.ident | T.integer | Token('(') + expr + ')' | call
    expr = Prio(                      # If ambiguous choose atom 1st, ...
        atom,
        Tokens("+ - ~") >> THIS,      # >> means right associative
        THIS << Tokens("* / // %") << THIS,
        THIS << Tokens("+ -") << THIS,# THIS means "expr" here
        THIS << (Tokens("== !=") | Keyword("is")) << THIS)
    expr["a"] = "I am a mapping too!"
    START = expr                      # Where the grammar must start
    COMMENTS = (                      # Allow C and Python comments
        Token(re="#(?:[^\r\n]*(?:\r\n?|\n\r?))") |
        Token(re="/[*](?:[^*]|[*][^/])*[*]/"))

parse_tree = ExprParser.parse("1 + /* a */ b + 3 * 4 is c(1, a)")
print(ExprParser.repr_parse_tree(parse_tree))
