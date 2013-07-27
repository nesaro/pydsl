from Pysec import Parser, choice, quoted_chars, group_chars, option_chars, digits, between, pair, spaces, match, quoted_collection

# json_choices is a hack to get around mutual recursion 
# a json is value is one of text, number, mapping, and collection
# text is any characters between quotes
# a number is like the regular expression -?[0-9]+(\.[0-9]+)?
# "parser >> Parser.lift(func)" means "pass the parsed value into func and return a new Parser"
# quoted_collection(start, space, inner, joiner, end)
#   means "a list of inner separated by joiner surrounded by start and end"
# we have to put a lot of "spaces" in since JSON allows lot of optional whitespace

json_choices = []
json         = choice(json_choices)
text         = quoted_chars("'", "'")
number       = group_chars([option_chars(["-"]), digits, option_chars([".", digits])]) >> Parser.lift(float)
joiner       = between(spaces, match(","), spaces)
mapping_pair = pair(text, spaces & match(":") & spaces & json)
collection   = quoted_collection("[", spaces, json,         joiner, "]") >> Parser.lift(list)
mapping      = quoted_collection("{", spaces, mapping_pair, joiner, "}") >> Parser.lift(dict)
json_choices.extend([text, number, mapping, collection])

print json.parseString("{'a' : -1.0, 'b' : 2.0, 'z' : {'c' : [1.0, [2.0, [3.0]]]}}")
