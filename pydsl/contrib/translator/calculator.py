__all__ = ['repository', 'iclass', 'root_rule', 'rules']
rules = """digit = anything:x ?(x in '0123456789')
number = <digit+>:ds -> int(ds)
expr = number:left ( '+' number:right -> left + right
                   | -> left)"""

root_rule="expr"

from pydsl.grammar.PEG import Sequence
repository={'string':Sequence.from_string('fas')}
iclass="parsley"

