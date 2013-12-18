#  Copyright (c) 1999-2000 John Aycock
#  
#  Permission is hereby granted, free of charge, to any person obtaining
#  a copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to
#  the following conditions:
#  
#  The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#  Based on Python 1.5.2 grammar.
#

from pydsl.external.spark import GenericParser

class CoreParser(GenericParser):
    def __init__(self, start):
        GenericParser.__init__(self, start)

    def typestring(self, token):
        return token.type

    def error(self, token):
        print("Syntax error at `%s' (line %s)" % (token, token.lineno))
        raise SystemExit

    def p_funcdef(self, args):
        '''
            funcdef ::= def NAME parameters : suite
        '''

    def p_parameters(self, args):
        '''
            parameters ::= ( varargslist )
            parameters ::= ( )
        '''

    def p_varargslist(self, args):
        '''
            varargslist ::= extraargs
            varargslist ::= primaryargs , extraargs
            varargslist ::= primaryargs opt_comma

            primaryargs ::= primaryargs , fpdef = test
            primaryargs ::= primaryargs , fpdef
            primaryargs ::= fpdef = test
            primaryargs ::= fpdef

            extraargs ::= * NAME
            extraargs ::= * NAME , ** NAME
            extraargs ::= * NAME , * * NAME
            extraargs ::= ** NAME
            extraargs ::= * * NAME
        '''

    def p_fpdef(self, args):
        '''
            fpdef ::= NAME
            fpdef ::= ( fplist )
        '''

    def p_fplist(self, args):
        '''
            fplist ::= bare_fplist opt_comma

            bare_fplist ::= bare_fplist , fpdef
            bare_fplist ::= fpdef
        '''

    def p_stmt(self, args):
        '''
            stmt ::= simple_stmt
            stmt ::= compound_stmt
        '''

    def p_simple_stmt(self, args):
        '''
            simple_stmt ::= small_stmt_list ; NEWLINE
            simple_stmt ::= small_stmt_list NEWLINE
        '''

    def p_small_stmt_list(self, args):
        '''
            small_stmt_list ::= small_stmt_list ; small_stmt
            small_stmt_list ::= small_stmt
        '''

    def p_small_stmt(self, args):
        '''
            small_stmt ::= expr_stmt
            small_stmt ::= print_stmt
            small_stmt ::= del_stmt
            small_stmt ::= pass_stmt
            small_stmt ::= flow_stmt
            small_stmt ::= import_stmt
            small_stmt ::= global_stmt
            small_stmt ::= exec_stmt
            small_stmt ::= assert_stmt
        '''

    def p_expr_stmt(self, args):
        '''
            expr_stmt ::= expr_stmt = testlist
            expr_stmt ::= testlist
        '''

    def p_print_stmt(self, args):
        '''
            print_stmt ::= print testlist
            print_stmt ::= print
        '''

    def p_del_stmt(self, args):
        '''
            del_stmt ::= del exprlist
        '''

    def p_pass_stmt(self, args):
        '''
            pass_stmt ::= pass
        '''

    def p_flow_stmt(self, args):
        '''
            flow_stmt ::= break_stmt
            flow_stmt ::= continue_stmt
            flow_stmt ::= return_stmt
            flow_stmt ::= raise_stmt
        '''

    def p_break_stmt(self, args):
        '''
            break_stmt ::= break
        '''

    def p_continue_stmt(self, args):
        '''
            continue_stmt ::= continue
        '''

    def p_return_stmt(self, args):
        '''
            return_stmt ::= return testlist
            return_stmt ::= return
        '''

    def p_raise_stmt(self, args):
        '''
            raise_stmt ::= raise test , test , test
            raise_stmt ::= raise test , test
            raise_stmt ::= raise test
            raise_stmt ::= raise
        '''

    def p_import_stmt(self, args):
        '''
            import_stmt ::= import dotted_name_list
            import_stmt ::= from dotted_name import *
            import_stmt ::= from dotted_name import name_list
        '''

    def p_dotted_name_list(self, args):
        '''
            dotted_name_list ::= dotted_name_list , dotted_name
            dotted_name_list ::= dotted_name
        '''

    def p_name_list(self, args):
        '''
            name_list ::= name_list , NAME
            name_list ::= NAME
        '''

    def p_dotted_name(self, args):
        '''
            dotted_name ::= dotted_name . NAME
            dotted_name ::= NAME
        '''

    def p_global_stmt(self, args):
        '''
            global_stmt ::= global name_list
        '''

    def p_exec_stmt(self, args):
        '''
            exec_stmt ::= exec expr in test , test
            exec_stmt ::= exec expr in test
            exec_stmt ::= exec expr
        '''

    def p_assert_stmt(self, args):
        '''
            assert_stmt ::= assert test , test
            assert_stmt ::= assert test
        '''

    def p_compound_stmt(self, args):
        '''
            compound_stmt ::= if_stmt
            compound_stmt ::= while_stmt
            compound_stmt ::= for_stmt
            compound_stmt ::= try_stmt
            compound_stmt ::= funcdef
            compound_stmt ::= classdef
        '''

    def p_if_stmt(self, args):
        '''
            if_stmt ::= if test : suite elif_clause_list opt_else_clause
            if_stmt ::= if test : suite opt_else_clause
        '''

    def p_elif_clause_list(self, args):
        '''
            elif_clause_list ::= elif_clause_list elif test : suite
            elif_clause_list ::= elif test : suite
        '''

    def p_opt_else_clause(self, args):
        '''
            opt_else_clause ::= else : suite
            opt_else_clause ::=
        '''

    def p_while_stmt(self, args):
        '''
            while_stmt ::= while test : suite opt_else_clause
        '''

    def p_for_stmt(self, args):
        '''
            for_stmt ::= for exprlist in testlist : suite opt_else_clause
        '''

    def p_try_stmt(self, args):
        '''
            try_stmt ::= try : suite except_clause_list opt_else_clause
            try_stmt ::= try : suite finally : suite
        '''

    def p_except_clause_list(self, args):
        '''
            except_clause_list ::= except_clause_list except_clause : suite
            except_clause_list ::= except_clause : suite
        '''

    def p_except_clause(self, args):
        '''
            except_clause ::= except test , test
            except_clause ::= except test
            except_clause ::= except
        '''

    def p_suite(self, args):
        '''
            suite ::= simple_stmt
            suite ::= NEWLINE INDENT stmt_list DEDENT
        '''

    def p_stmt_list(self, args):
        '''
            stmt_list ::= stmt_list stmt
            stmt_list ::= stmt
        '''

    def p_test(self, args):
        '''
            test ::= lambdef
            test ::= or_test
        '''

    def p_or_test(self, args):
        '''
            or_test ::= or_test or and_test
            or_test ::= and_test
        '''

    def p_and_test(self, args):
        '''
            and_test ::= and_test and not_test
            and_test ::= not_test
        '''

    def p_not_test(self, args):
        '''
            not_test ::= not not_test
            not_test ::= comparison
        '''

    def p_comparison(self, args):
        '''
            comparison ::= comparison comp_op expr
            comparison ::= expr
        '''

    def p_comp_op(self, args):
        '''
            comp_op ::= <
            comp_op ::= >
            comp_op ::= ==
            comp_op ::= >=
            comp_op ::= <=
            comp_op ::= <>
            comp_op ::= !=
            comp_op ::= in
            comp_op ::= not in
            comp_op ::= is
            comp_op ::= is not
        '''

    def p_expr(self, args):
        '''
            expr ::= expr | xor_expr
            expr ::= xor_expr
        '''

    def p_xor_expr(self, args):
        '''
            xor_expr ::= xor_expr ^ and_expr
            xor_expr ::= and_expr
        '''

    def p_and_expr(self, args):
        '''
            and_expr ::= and_expr & shift_expr
            and_expr ::= shift_expr
        '''

    def p_shift_expr(self, args):
        '''
            shift_expr ::= shift_expr << arith_expr
            shift_expr ::= shift_expr >> arith_expr
            shift_expr ::= arith_expr
        '''

    def p_arith_expr(self, args):
        '''
            arith_expr ::= arith_expr + term
            arith_expr ::= arith_expr - term
            arith_expr ::= term
        '''

    def p_term(self, args):
        '''
            term ::= term * factor
            term ::= term / factor
            term ::= term % factor
            term ::= factor
        '''

    def p_factor(self, args):
        '''
            factor ::= + factor
            factor ::= - factor
            factor ::= ~ factor
            factor ::= power
        '''

    def p_power(self, args):
        '''
            power ::= atom trailer_list power_list
            power ::= atom trailer_list
            power ::= atom power_list
            power ::= atom
        '''

    def p_trailer_list(self, args):
        '''
            trailer_list ::= trailer_list trailer
            trailer_list ::= trailer
        '''

    def p_power_list(self, args):
        '''
            power_list ::= power_list ** factor
            power_list ::= ** factor
        '''

    def p_atom(self, args):
        '''
            atom ::= ( testlist )
            atom ::= ( )
            atom ::= [ testlist ]
            atom ::= [ ]
            atom ::= { dictmaker }
            atom ::= { }
            atom ::= ` testlist `
            atom ::= NAME
            atom ::= NUMBER
            atom ::= string_list
        '''

    def p_string_list(self, args):
        '''
            string_list ::= string_list STRING
            string_list ::= STRING
        '''

    def p_lambdef(self, args):
        '''
            lambdef ::= lambda varargslist : test
            lambdef ::= lambda : test
        '''

    def p_trailer(self, args):
        '''
            trailer ::= ( arglist )
            trailer ::= ( )
            trailer ::= [ subscriptlist ]
            trailer ::= . NAME
        '''

    def p_subscriptlist(self, args):
        '''
            subscriptlist ::= bare_subscriptlist opt_comma

            bare_subscriptlist ::= bare_subscriptlist , subscript
            bare_subscriptlist ::= subscript
        '''

    def p_subscript(self, args):
        '''
            subscript ::= . . .
            subscript ::= test
            subscript ::= opt_test : opt_test
            subscript ::= opt_test : opt_test : opt_test
        '''

    def p_opt_test(self, args):
        '''
            opt_test ::= test
            opt_test ::=
        '''

    def p_opt_comma(self, args):
        '''
            opt_comma ::= ,
            opt_comma ::=
        '''

    def p_exprlist(self, args):
        '''
            exprlist ::= bare_exprlist opt_comma

            bare_exprlist ::= bare_exprlist , expr
            bare_exprlist ::= expr
        '''

    def p_testlist(self, args):
        '''
            testlist ::= bare_testlist opt_comma

            bare_testlist ::= bare_testlist , test
            bare_testlist ::= test
        '''

    def p_dictmaker(self, args):
        '''
            dictmaker ::= bare_dictmaker opt_comma

            bare_dictmaker ::= bare_dictmaker , test : test
            bare_dictmaker ::= test : test
        '''

    def p_classdef(self, args):
        '''
            classdef ::= class NAME ( testlist ) : suite
            classdef ::= class NAME : suite
        '''

    def p_arglist(self, args):
        '''
            arglist ::= bare_arglist opt_comma

            bare_arglist ::= bare_arglist , argument
            bare_arglist ::= argument
        '''

    def p_argument(self, args):
        '''
            argument ::= test = test
            argument ::= test
        '''

class SingleInputParser(CoreParser):
    def __init__(self):
        CoreParser.__init__(self, 'single_input')

    def p_single_input(self, args):
        '''
            single_input ::= NEWLINE
            single_input ::= simple_stmt
            single_input ::= compound_stmt NEWLINE
        '''

class FileInputParser(CoreParser):
    def __init__(self):
        CoreParser.__init__(self, 'file_input')

    def p_file_input(self, args):
        '''
            file_input ::= file_contents ENDMARKER
        '''

    def p_file_contents(self, args):
        '''
            file_contents ::= file_contents NEWLINE
            file_contents ::= file_contents stmt
            file_contents ::=
        '''

class EvalInputParser(CoreParser):
    def __init__(self):
        CoreParser.__init__(self, 'eval_input')

    def p_eval_input(self, args):
        '''
            eval_input ::= testlist newlines ENDMARKER
            eval_input ::= testlist ENDMARKER

            newlines ::= newlines NEWLINE
            newlines ::= NEWLINE
        '''

def parse(tokens):
    parser = FileInputParser()
    return parser.parse(tokens)
