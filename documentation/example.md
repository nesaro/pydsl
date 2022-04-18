```python
from pydsl.file.BNF import load_bnf_file
from pydsl.file.python import load_python_file
from pydsl.translator import translator_factory
truefalse = load_bnf_file('pydsl/contrib/grammar/TrueFalse.bnf')
grammardefinition = load_bnf_file('pydsl/contrib/grammar/LogicalExpression.bnf', {'TrueFalse':truefalse})
grammardefinition.alphabet # Returns the alphabet used by this grammar
grammardefinition.minsize
grammardefinition.maxsize
from pydsl.check import check
check(grammardefinition,['(']) # returns True or False
from pydsl.parser import parse
parse(grammardefinition,[')']) # returns a ParseTree
from pydsl.extract import extract
extract(grammardefinition,'abc()abc') # returns ('False',3,11)
solver = translator_factory(load_python_file('pydsl/contrib/translator/echo.py'))
mystring = "True||False"
result = solver(mystring)
print(result)
```

