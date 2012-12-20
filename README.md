DESCRIPTION
===========

pydsl is a language library written in python
The main idea is to allow an easy way to define, use and combine DSLs to create programs and provide tools around them.

pydsl support several grammar specification formats:
 * regular expressions
 * pydsl BNF format
 * ANLTR .g format (not supported yet)
 * mongo database query dictionaries
 * python ply module (only check support)

each grammar definition have the following properties:
 * enum(gd): yields a list of accepted words
 * first(gd): yields a list of the first accepted subword/char
 * minsize(gd): length of the smaller accepted word
 * maxsize(gd): length of the biggest accepted word

pydsl offer a set of functionalities that use _grammar definitions_
 * validate(gd, input): test the input string against the spec. In case of failure, it returns a list of errors
 * partition(gd, input, tag): returns the parts of the input according to a tag

alphabet abstraction is also available. Alphabets are a set of symbols that are recognized using a regular grammar. Properties:
 * symbols(ad): return the list of allowed symbols for this alphabet

functionalities that use _alphabets_:
 * lexer(ad, input): Generates a tokenlist from a string (it is a special case of translate)
 * mapper(ad, input): Converts a tokenlist from an alphabet into another alphabet
 
functionalities that use both _alphabets_ and _grammar definitions_:
 * guess(input, [gd]): returns a list of _grammar definitions_ that are compatible with the input
 * distance(gd, input1, input2): returns the distance between two inputs according to _grammar definition_
 * check(d, input): test the input string against the spec
 * extract(gd, input): extract all the slices of the input that are accepted by the definition 

translation functionalities
 * translate(td, input): generic translator
   * ast(astdefinition, input): creates an abstract syntax tree according to astdefinition
   * sdt( sdt, ast): Performs an AST translation using a Syntax Directed Translator

pydsl also offers library related functionalities:
 * search(query): search for an element within a memory
 * info(identifier): returns information about the element
 * translations(identifier): returns a list of available translators for identifier

INSTALLATION
============
 * disttools:
   * python3 setup.py install
 * pip:
   * pip install git+http://github.com/nesaro/pydsl.git

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

    from pydsl.Memory.Storage.Directory import DirStorage
    from pydsl.Guess import Guesser
    a = DirStorage("directory/")
    guess = Guesser([a])
    guess('string')

Using contrib
-------------------
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


CONTRIB
=======

contrib directory contains several types of elements. Those elements are either imported by colony or used as a function argument for their binaries.

 * board: Boards are Functions, therefore they can be used as an argument for:
   * translate: translate -e input -t boardname
 * grammar: Grammar are Types; they can be used with the following programs:
   * check: check -e expression grammarname
   * extract: extract -e expression grammarname
   * validate: extract -e expression grammarname
 * procedure: procedure are functions, but have no input 
   * translate: translate -t procedurename
 * board: Transformer are Functions too:
   * translate: translate -e input -t functionname
 * dict/filetype.dict: A list of filetypes, which are types
 * dict/refexp.dict: A list of Regular expressions, which are types

search program will find any element within the library.
info gives a summary for an element
guess returns a list of the types that match the input element


REQUIREMENTS
============
 * python >= 2.7
 * optional: ply library ( http://www.dabeaz.com/ply/ )

HELP
====
 * http://github.com/nesaro/pydsl
 * http://pydsl.blogspot.co.uk
 * nesaro@gmail.com

LICENSE
=======
GPLv3, see LICENSE file

ABOUT
=====
pydsl is a formal language framework.
Copyright (C) 2008-2012 Nestor Arocha (nesaro@gmail.com)
