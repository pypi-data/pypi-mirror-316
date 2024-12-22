import ply.lex as lex
import ply.yacc as yacc

# Token definitions for the lexer
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Token regex rules
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Token for numbers
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)  # Convert to a float
    return t

# Ignored characters (e.g., spaces)
t_ignore = ' \t'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Grammar rules for the parser
def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | LPAREN expression RPAREN'''
    if len(p) == 2:  # NUMBER
        p[0] = p[1]
    else:  # LPAREN expression RPAREN
        p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

# Function to evaluate an expression
def evaluate_expression(expression):
    return parser.parse(expression)

# Example usage
while True:
    try:
        expr = input("Enter an expression (or 'exit' to quit): ")
        if expr.lower() == 'exit':
            break
        result = evaluate_expression(expr)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
