#Transformador teorico que obtiene las diferencias entre dos palabras aceptadas de una gramática.
#A cada Grammar le pide el arbol u otra cosa para poder evaluar las diferencias

inputdic = { "grammaname":"cstring", "value1":"cstring", "value2":"cstring"}
outputdic = {"output":"cstring"} #TODO: Ver que gramatica se puede definir
iclass = "PythonTransformer"

def diff(content1, content2, grammarlist = [], alphabetlist = []):
    result = {}
    if not grammarlist and not alphabetlist:
        guess1 = set(guess(content1))
        guess2 = set(guess(content2))
        grammarlist = list(guess1.union(guess2))
    for al in alphabetlist:
        tknlist1 = al.parse(content1)
        tknlist2 = al.parse(content2)
        result[al] = string_distance(tknlist1, tknlist2)
    for grammar in grammarlist:
        if is_bnf_grammar:
            tree1 = grammar.to_parse_tree(content1)
            tree2 = grammar.to_parse_tree(content2)
            diff = load_diff("tree")
            result[grammar + "_tree"] = diff(tree1, tree2)
        diff = load_diff(grammar)
        result[grammar] = diff(content1, content2)
    return result
