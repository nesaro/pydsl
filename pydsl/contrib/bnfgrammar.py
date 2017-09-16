"""BNF grammars for testing"""

from pydsl.grammar.symbol import TerminalSymbol, NonTerminalSymbol, NullSymbol
from pydsl.grammar.BNF import Production, BNFGrammar
from pydsl.file.BNF import strlist_to_production_set
from pydsl.file.python import load_python_file
from pydsl.grammar.definition import String, RegularExpression

leftrecursive=["S ::= E","E ::= E dot | dot","dot := String,."]
rightrecursive=["S ::= E","E ::= dot E | dot","dot := String,."]
centerrecursive=["S ::= E","E ::= dot E dot | dot","dot := String,."]

#productionset0 definition

symbol1 = TerminalSymbol(String("S"))
symbol2 = TerminalSymbol(String("R"))
final1 = NonTerminalSymbol("exp")
rule1 = Production([final1], (symbol1, symbol2))
productionset0 = BNFGrammar(final1, (rule1,symbol1,symbol2))
p0good = "SR"
p0bad = "RS"


#productionset1 definition
symbol1 = TerminalSymbol(String("S"))
symbol2 = TerminalSymbol(String("R"))
symbol3 = TerminalSymbol(String(":"))
symbol4 = TerminalSymbol(RegularExpression("^[0123456789]*$"))
symbol5 = TerminalSymbol(load_python_file('pydsl/contrib/grammar/cstring.py'))
final1 = NonTerminalSymbol("storeexp") 
final2 = NonTerminalSymbol("retrieveexp") 
final3 = NonTerminalSymbol("exp")
rule1 = Production([final1], (symbol1, symbol3, symbol5))
rule2 = Production([final2], (symbol2, symbol3, symbol4))
rule3 = Production([final3], [final1])
rule4 = Production([final3], [final2])
rulelist = (rule1, rule2, rule3, rule4, symbol1, symbol2, symbol3, symbol4, symbol5)
productionset1 = BNFGrammar(final3, rulelist)

#productionset2 definition
symbola = TerminalSymbol(String("A"))
symbolb = TerminalSymbol(String("B"))
nonterminal = NonTerminalSymbol("res")
rulea = Production ((nonterminal,), (symbola, NullSymbol(), symbolb))
productionset2 = BNFGrammar(nonterminal, (rulea, symbola, symbolb))
productionsetlr = strlist_to_production_set(leftrecursive)
productionsetrr = strlist_to_production_set(rightrecursive)
productionsetcr = strlist_to_production_set(centerrecursive)

#arithmetic


arithmetic=["E ::= E plus T | T", "T ::= T times F | F" ,"F ::= open_parenthesis E close_parenthesis | id", "id := String,123" , "plus := String,+", "times := String,*", "open_parenthesis := String,(","close_parenthesis := String,)"]
productionset_arithmetic = strlist_to_production_set(arithmetic, start_symbol= "E")

addition=["S ::= E","E ::= E plus F | F" ,"F ::= open_parenthesis E close_parenthesis | id", "id := String,123" , "plus := String,+", "open_parenthesis := String,(","close_parenthesis := String,)"]
productionset_addition = strlist_to_production_set(addition)
#tokenlist definition
string1 = "S:a"
string2 = "S:"
string3 = "AB"
string4 = "AAB"
string5 = "ACB"
dots = "....."
