DESCRIPTION
===========

pydsl is a language library written in python. It provides some verbs for Grammars.

    from pydsl.file.BNF import load_bnf_file
    grammardefinition = loand_bnf_file('myfile.bnf')
    grammardefinition.alphabet # Returns the alphabet used by this grammar
    grammardefinition.minsize
    grammardefinition.maxsize 
    grammardefinition.enumerate # Returns a generator that generates every accepted word

    from pydsl.check import check
    check(grammardefinition,'mystring') # returns True or False

    from pydsl.parser import parse
    parse(grammardefinition,'mystring') # returns a ParseTree

    from pydsl.extract import extract
    extract(grammardefinition,'abcmystringabc') # returns ('mystring',3,11)

FORMATS
=======

Functions
---------

| Format  |Check|Match|Search|Split|Extract|Translate|Validate|Diff|
| ------- |:---:|-----|------|-----|:-----:|:-------:|:------:|----|
| BNF     | V   |     |      |     |V      | Parse   | V      |    |
| regexp  | V   |     |      |     |V      | X       |        |    |
| ply     | V   |     |      |     |V      | V       |        |    |
| parsley | V   |     |      |     |V      | V       |        |    |
|pyparsing| V   |     |      |     |V      |         |        |    |

Properties
----------

| Format  |First|Min|Max|Enumerate|
| ------- |:---:|---|---|---------|
| BNF     | V   |   |   |         |
| regexp  |     |   |   |         |
| ply     |     |   |   |         |
| parsley |     |   |   |         |
|pyparsing|     |   |   |         |


INSTALLATION
============
 * disttools:
   * python3 setup.py install
 * pip:
   * pip install pydsl

CONTRIBUTIONS
=============
 * check existing issues: https://github.com/nesaro/pydsl
 * read the project's blog: http://pydsl.blogspot.co.uk
 * pull requests :)


REQUIREMENTS
============
 * python >= 3.4
 * optional: ply library ( http://www.dabeaz.com/ply/ )

ABOUT
=====
Copyright (C) 2008-2015 Nestor Arocha (nesaro@gmail.com)
