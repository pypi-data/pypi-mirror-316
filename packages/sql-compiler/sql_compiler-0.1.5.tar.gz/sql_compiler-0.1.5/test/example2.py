from ply import lex, yacc

# --- Tokenizer ---
class Lexer:
    tokens = (
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
        'NAME', 'NUMBER'
    )

    # Ignored characters
    t_ignore = ' \t'

    # Token rules
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ignore_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenize(self, data):
        self.lexer.input(data)
        return list(self.lexer)

# --- Parser ---
class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    # Grammar rules
    def p_expression_binop(self, p):
        '''
        expression : term PLUS term
                   | term MINUS term
        '''
        p[0] = ('binop', p[2], p[1], p[3])

    def p_expression_term(self, p):
        '''
        expression : term
        '''
        p[0] = p[1]

    def p_term_binop(self, p):
        '''
        term : factor TIMES factor
             | factor DIVIDE factor
        '''
        p[0] = ('binop', p[2], p[1], p[3])

    def p_term_factor(self, p):
        '''
        term : factor
        '''
        p[0] = p[1]

    def p_factor_number(self, p):
        '''
        factor : NUMBER
        '''
        p[0] = ('number', p[1])

    def p_factor_name(self, p):
        '''
        factor : NAME
        '''
        p[0] = ('name', p[1])

    def p_factor_unary(self, p):
        '''
        factor : PLUS factor
               | MINUS factor
        '''
        p[0] = ('unary', p[1], p[2])

    def p_factor_grouped(self, p):
        '''
        factor : LPAREN expression RPAREN
        '''
        p[0] = ('grouped', p[2])

    def p_error(self, p):
        print(f"Syntax error at {p.value!r}")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

# --- Example Usage ---
if __name__ == "__main__":
    parser = Parser()
    input_data = "2 * 3 + 4 * (5 - x)"
    result = parser.parse(input_data)
    print(f"Input: {input_data}")
    print(f"AST: {result}")
