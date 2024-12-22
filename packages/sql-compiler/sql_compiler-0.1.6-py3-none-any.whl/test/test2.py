from rply import LexerGenerator, ParserGenerator

# Lexer
class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Define tokens for the new grammar
        self.lexer.add('ASSIGN', r'=')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        self.lexer.add('LPAREN', r'\(')
        self.lexer.add('RPAREN', r'\)')
        self.lexer.add('NUMBER', r'\d*\.\d+|\d+\.?')  # Support for numbers
        self.lexer.add('ID', r'[a-zA-Z_][a-zA-Z0-9_]*')  # Variable names
        self.lexer.ignore(r'\s+')  # Ignore whitespace

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()

    def tokenize(self, text):
        """Tokenize input text and return a list of tokens"""
        lexer = self.get_lexer()
        return list(lexer.lex(text))

# Abstract Syntax Tree (AST)
class AST:
    class Number:
        def __init__(self, value):
            self.value = float(value)
        
        def eval(self, env):
            return self.value

    class Variable:
        def __init__(self, name):
            self.name = name
        
        def eval(self, env):
            if self.name not in env:
                raise NameError(f"Variable '{self.name}' not defined")
            return env[self.name]

    class Assignment:
        def __init__(self, name, expression):
            self.name = name
            self.expression = expression
        
        def eval(self, env):
            env[self.name] = self.expression.eval(env)
            return env[self.name]

    class BinaryOp:
        def __init__(self, left, right):
            self.left = left
            self.right = right

    class Add(BinaryOp):
        def eval(self, env):
            return self.left.eval(env) + self.right.eval(env)

    class Subtract(BinaryOp):
        def eval(self, env):
            return self.left.eval(env) - self.right.eval(env)

    class Multiply(BinaryOp):
        def eval(self, env):
            return self.left.eval(env) * self.right.eval(env)

    class Divide(BinaryOp):
        def eval(self, env):
            right_val = self.right.eval(env)
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return self.left.eval(env) / right_val

# Parser
class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            ['ASSIGN', 'ID', 'NUMBER', 'PLUS', 'MINUS', 'MUL', 'DIV', 
             'LPAREN', 'RPAREN'],
        )
        self._define_grammar()

    def _define_grammar(self):
        @self.pg.production('statement : ID ASSIGN expression')
        def statement_assign(p):
            return AST.Assignment(p[0].value, p[2])

        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression MINUS expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_binop(p):
            left, op, right = p[0], p[1], p[2]
            if op.gettokentype() == 'PLUS':
                return AST.Add(left, right)
            elif op.gettokentype() == 'MINUS':
                return AST.Subtract(left, right)
            elif op.gettokentype() == 'MUL':
                return AST.Multiply(left, right)
            elif op.gettokentype() == 'DIV':
                return AST.Divide(left, right)

        @self.pg.production('expression : NUMBER')
        def expression_number(p):
            return AST.Number(p[0].value)

        @self.pg.production('expression : ID')
        def expression_variable(p):
            return AST.Variable(p[0].value)

        @self.pg.production('expression : LPAREN expression RPAREN')
        def expression_paren(p):
            return p[1]

        @self.pg.error
        def error_handler(token):
            raise ValueError(f"Syntax error at token: {token}")

    def get_parser(self):
        return self.pg.build()

# Interpreter
class Interpreter:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self._parser = self.parser.get_parser()
        self.env = {}  # Environment for storing variables

    def evaluate(self, text):
        try:
            # Tokenize
            tokens = self.lexer.tokenize(text)
            
            # Parse
            ast = self._parser.parse(iter(tokens))
            
            # Evaluate
            return ast.eval(self.env)
        except Exception as e:
            return f"Error: {str(e)}"

# Test
interpreter = Interpreter()

test_inputs = [
    "x = 3 + 4 * 2",
    "y = (3 + 4) * 2",
    "z = x + y",
    "x",  # Accessing variable
    "z"   # Accessing variable
]

for test in test_inputs:
    print(f"\nInput: {test}")
    result = interpreter.evaluate(test)
    print(f"Result: {result}")
