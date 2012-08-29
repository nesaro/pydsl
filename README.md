DESCRIPTION
===========

pydsl is an environment for creating and using formal languages. 
The main idea is to allow an easy way to define, use and combine DSLs to create programs.
pydsl support several grammar specification formats:
 * regular expressions
 * pydsl BNF format
 * ANLTR .g format (not supported yet)
 * mongo database query dictionaries

each grammar definition have the following properties:
 * enum(gd): yields a list of accepted words
 * first(gd): yields a list of the first accepted subword/char
 * minsize(gd): length of the smaller accepted word
 * maxsize(gd): length of the biggest accepted word

pydsl offer a set of functionalities that use _grammar definitions_
 * check(gd, input): test the input string against the spec
 * validate(gd, input): test the input string against the spec. In case of failure, it returns a list of errors
 * guess(input, [gd]): returns a list of _grammar definitions_ that are compatible with the input
 * partition(gd, input, tag): returns the parts of the input according to a tag
 * extract(gd, input): extract all the slices of the input that are accepted by _grammar definition_
 * distance(gd, input1, input2): returns the distance between two inputs according to _grammar definition_
 * translate(gd, input): generic translator
   * ast(astdefinition, input): creates an abstract syntax tree according to astdefinition
   * sdt( sdt, ast): Performs an AST translation using a Syntax Directed
   Translator

It also offers library related functionalities:
 * search(query): search for an element within a memory
 * info(identifier): returns information about the element
 * translations(identifier): returns a list of available translators for identifier

INSTALLATION
============
 * disttools: python3 setup.py install
 * pip: pip install git+http://github.com/nesaro/pydsl.git

USAGE
=====
To use pydsl as a library for your code, you can:

Loading content from files
--------------------------
    from pydsl.Memory.Storage.File.BNF import load_bnf_file
    grammardefinition = loand_bnf_file('myfile.bnf')
    from pydsl.Memory.Loader import *
    mychecker = load_checker(grammardefinition)
    mychecker('mystring') # returns True or False

Loading content from a directory
--------------------------------
First store your grammar definitions in a directory,

    from pydsl.Memory.Storage.Directory.Grammar import GrammarDirStorage
    from pydsl.Guess import Guesser
    a = GrammarDirStorage("directory/")
    guess = Guesser([a])
    guess('string')

Using pydsl-contrib
-------------------
 * Download pydsl-contrib repositorie from github
 * install with python3 setup.py install
 * use default libraries and transformers

code:

    from pydsl.Memory.Loader import *
    mychecker = load_checker(integer)
    mytransformer = load_function('inttohex')
    result = a({'input':'123'})

BINARIES
========
Memory Management
-----------------
 * info.py: Retrieves an element from memory and shows a summary
 * search.py: Searchs memory 

Grammars
--------
 * check.py: Checks if input data belongs to a grammar
 * guess:py: Determines input data type
 * validate.py: Perform a validation routine for user data according to a grammar

Functions
---------
 * translate.py: Process user input using a function


REQUIREMENTS
============
 * python >= 3.0
 * pydsl contrib package ( https://github.com/nesaro/pydsl-contrib )

HELP
====
 * http://github.com/nesaro/pydsl
 * nesaro@gmail.com

LICENSE
=======
GPLv3, see LICENSE file

ABOUT
=====
pydsl is a formal and natural language framework.
Copyright (C) 2008-2012 Nestor Arocha (nesaro@gmail.com)
