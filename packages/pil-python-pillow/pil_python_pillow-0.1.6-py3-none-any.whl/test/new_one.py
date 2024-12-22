import ply.lex as lex
from antlr4 import *
from lark import Lark, Transformer
from ExprLexer import ExprLexer
from ExprParser import ExprParser

# Step 1: Tokenization with PLY
# Define tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Token rules
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Step 2: Parsing with ANTLR
# Define Grammar File Inline (Save this as `Expr.g4` for ANTLR):
grammar = """
grammar Expr;

expr: expr ('+'|'-') term   # AddSub
    | term                  # SingleTerm
    ;

term: term ('*'|'/') factor # MulDiv
    | factor                # SingleFactor
    ;

factor: NUMBER              # Number
      | '(' expr ')'        # Parens
      ;

NUMBER: [0-9]+;
WS: [ \t\n\r]+ -> skip;
"""

# Generate the parser using ANTLR (Run this command manually):
# antlr4 -Dlanguage=Python3 Expr.g4

# Include the generated Lexer and Parser (make sure `ExprLexer` and `ExprParser` are in the same folder)


def parse_expression_with_antlr(input_text):
    lexer = ExprLexer(InputStream(input_text))
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.expr()  # Start rule
    return tree

# Step 3: Evaluation with Lark
lark_grammar = """
    start: expr
    expr: expr "+" term   -> add
        | expr "-" term   -> sub
        | term
    term: term "*" factor -> mul
        | term "/" factor -> div
        | factor
    factor: NUMBER        -> number
          | "(" expr ")"
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

class EvaluateExpression(Transformer):
    def add(self, args):
        return args[0] + args[1]
    
    def sub(self, args):
        return args[0] - args[1]
    
    def mul(self, args):
        return args[0] * args[1]
    
    def div(self, args):
        return args[0] / args[1]
    
    def number(self, args):
        return int(args[0])

lark_parser = Lark(lark_grammar, parser='lalr', transformer=EvaluateExpression())

def evaluate_with_lark(input_expr):
    return lark_parser.parse(input_expr)

# Step 4: Compiler Workflow
def compile_and_run(input_code):
    # Tokenization with PLY
    lexer.input(input_code)
    tokens = list(lexer)
    print("Tokens:", tokens)
    
    # Parse with ANTLR
    tree = parse_expression_with_antlr(input_code)
    print("ANTLR Parse Tree:", tree.toStringTree())

    # Evaluate with Lark
    result = evaluate_with_lark(input_code)
    return result

# Example Usage
if __name__ == "__main__":
    while True:
        try:
            code = input("Enter an expression (or 'exit' to quit): ")
            if code.lower() == 'exit':
                break
            output = compile_and_run(code)
            print(f"Output: {output}")
        except Exception as e:
            print(f"Error: {e}")
