from pydsl.File.BNF import strlist_to_production_set
from pydsl.Grammar import RegularExpression
from pydsl.Parser.LL import LL1RecursiveDescentParser

def tree_translator(tree):
    from pydsl.Grammar.Symbol import NonTerminalSymbol
    if tree.symbol == NonTerminalSymbol("E"):
        return int(str(tree.childlist[0].content)) + int(str(tree.childlist[2].content))
    elif len(tree.childlist) == 1:
        return tree_translator(tree.childlist[0])
    else:
        raise Exception
            

grammar_def = [
        "S ::= E",
        "E ::= number operator number",
        "number := Word,integer,max",
        "operator := String,+",
        ]
repository = {'integer':RegularExpression("^[0123456789]*$")}
production_set = strlist_to_production_set(grammar_def, repository)
rdp = LL1RecursiveDescentParser(production_set)


def translator(data):
    parse_tree = rdp(data)
    return tree_translator(parse_tree[0])

