"""
Parsing sample

To parse we're giving a text to parse and an thing with a grammar. The default
setting includes skipping of whitespace, so we don't need to take care of that.

The comment parameter is set to C style /* comments */

>>> f = parse("int f(int a, long b) { do_this; do_that; }", Function, comment=comment_c)

Because function has a name() in its grammar, we can access this now as an
attribute. With Python 2.7 this gives Symbol(u'f'), with Python 3.2 it gives Symbol('f'):

>>> f.name
Symbol(...'f')

A Function has an Attribute "parms" in its grammar, which directs to class
Parameters.

>>> f.parms
Parameters([(Symbol(...'a'), <__main__.Parameter object at 0x...>), (Symbol(...'b'), <__main__.Parameter object at 0x...>), ])

Because Parameters is a Namespace, we can access its content by name.

>>> f.parms["a"]
<__main__.Parameter object at 0x...>

Its content are Parameter instances. Parameter has an Attribute "typing".

>>> f.parms["b"].typing
Type(...'long')

The Instructions of our small sample are just words. Because Function is a
List, we can access them one by one.

>>> f
Function([...'do_this', ...'do_that'], name=Symbol(...'f'))
>>> print("f is " + repr(f[0]))
f is ...'do_this'

The result can be composed to a text again.

>>> f.append(Instruction("do_something_else"))
>>> print(compose(f))
int f(int a, long b)
{
    /* on level 1 */
    do_this;
    /* on level 1 */
    do_that;
    /* on level 1 */
    do_something_else;
}
...

pyPEG contains an XML backend, too:

>>> del f[2]
>>> from pypeg2.xmlast import thing2xml
>>> xml = thing2xml(f, pretty=True)
>>> print(xml.decode())
<Function typing="int" name="f">
  <Parameters>
    <Parameter typing="int" name="a"/>
    <Parameter typing="long" name="b"/>
  </Parameters>
  <Instruction>do_this</Instruction>
  <Instruction>do_that</Instruction>
</Function>
...

The XML backend can read XML text and create things:

>>> from pypeg2.xmlast import xml2thing
>>> xml = b'<Function typing="long" name="g"><Parameters><Parameter name="x" typing="int"/></Parameters><Instruction>return</Instruction></Function>'
>>> g = xml2thing(xml, globals())
>>> g.name
Symbol(...'g')
>>> g.typing
Type(...'long')
>>> g.parms["x"].typing
Type(...'int')
>>> print("g[0] is " + repr(g[0]))
g[0] is ...'return'
"""

from __future__ import unicode_literals, print_function
from pypeg2 import *

# A Symbol can be an arbitrary word or one word of an Enum.
# In this easy example there is an Enum.

class Type(Keyword):
    grammar = Enum( K("int"), K("long") )

# Parsing attributes adds them to the resulting thing.
# blank is a callback function. Callback functions are being executed by
# compose(). parse() ignores callback functions. blank inserts " ".
# name() generates a name attribute.

class Parameter(object):
    grammar = attr("typing", Type), blank, name()

# A Namespace is a container for named things.
# csl() creates the grammar for a comma separated list.

class Parameters(Namespace):
    grammar = optional(csl(Parameter))

# This is an example for a user defined callback function, heading().
# endl is a special callback function. It is never executed. Instead it
# triggers the indention system of compose() and will be replaced by "\n".

class Instruction(str):
    def heading(self, parser):
        return "/* on level " + str(parser.indention_level) + " */", endl

    grammar = heading, word, ";", endl

# indent() is a function which marks things for being indented by compose().
# indent() raises the indention level by 1 for each thing which is inside.

block = "{", endl, maybe_some(indent(Instruction)), "}", endl

# If a thing is a List, then parsed things are being put into.

class Function(List):
    grammar = attr("typing", Type), blank, name(), "(", attr("parms", Parameters), ")", endl, block

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=(doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE))
